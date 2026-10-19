# run_08_fixes.py: part 8 of 18 of engine._run, the life loop.
# The many-lives fixes, prison ties, the world's effects for the story, option causes, the pause state.
# Lines here are _run's own, unchanged and at their own indent: engine.py joins the parts in order (engine.RUN_PARTS)
# and compiles them as one, so a name used here may be set in an earlier part. Never import or run it alone.
    # v22.5, the many-lives fixes (each off unless its switch is set; none draws from the run's own random stream)
    SET_ON = P["set_age"] is not None                     # F14: colours settle with age
    settle_f = np.ones(N)                                 # this week's factor on plasticity (the game's V2 can read it)
    if SET_ON:
        SET_A, SET_F = np.asarray(P["set_age"], float).T
        set_bu = np.zeros(N)                              # the person's usual openness
    UPM_ = None if P["up_mix"] is None else np.asarray(P["up_mix"], float) / np.sum(P["up_mix"])   # F15: the start's lean
    UPL_ON = UPM_ is not None and bool(P["up_lean"] or P["up_self"] or P["up_ease"])
    if UPL_ON:
        if P["up_fam"] and not WON:   # each household's own ways (N x C)
            wp_ = np.asarray(P["world_profile"], float)
            fam = np.random.default_rng([int(seed), 1515]).dirichlet(P["up_conc"] * C * wp_ / wp_.sum(), N)
            UPM_ = (1 - P["up_fam"]) * UPM_ + P["up_fam"] * fam
        UPD_ = UPM_ - 0.2; UPN_ = np.maximum((UPD_ * UPD_).sum(-1), 1e-9) if UPM_.ndim > 1 else max(float(UPD_ @ UPD_), 1e-9)
        up_oy = np.zeros((N, C)); up_oz = np.zeros((N, C))   # what the start's pulls have added to the want and to who they are
        UP_DEC = 1 - 0.5 ** (1 / (52 * P["up_half"]))         # which fades by half every up_half years from up_from
        def up_short(v):
            """F15: how far a pie (N x C) falls short of the lean the start still leaves, 0 to 1 of the full lean."""
            return _uclip((P["up_l0"] * upf_ - (((v - 0.2) * UPD_).sum(-1) if UPM_.ndim > 1 else (v - 0.2) @ UPD_) / UPN_) / P["up_l0"], 0, 1)
    DS_ON = bool(P["drv_self"]) and "DRVN" in L          # F9: the drivers' mean taken out in the run itself
    DRVN_ = np.asarray(L["DRVN"], float) if DS_ON else None
    PS_ON = P["par_split"] is not None                    # F9: a breakup and a home together
    if PS_ON:
        PS_SOFT = np.isin(np.asarray(ROOT), [i_ for i_, nm_ in enumerate(L["names"]) if nm_ in SPLIT_SOFT])
        ps_rng = np.random.default_rng([int(seed), 1709])
    PA_ON = P["par_age"] is not None                      # F9: partnerships by age
    if PA_ON:
        PA_A, PA_F = np.asarray(P["par_age"], float).T
    JM_ON = P["job_move"] is not None                     # F9.19: changing employer
    if JM_ON:
        JM_A, JM_F = np.asarray(P["job_move"], float).T
        jm_rng = np.random.default_rng([int(seed), 1713])
    LON_ON = P["lone"] is not None                        # F9.39: a spell of loneliness
    if LON_ON:
        LO_ = dict(P["lone"]); LA_, LF_ = np.asarray(LO_["age"], float).T
        lon_rng = np.random.default_rng([int(seed), 1721]); lone = np.zeros(N, bool)
    LP_ON = P["low_pay"] is not None                      # F9.38: each job's pay
    if LP_ON:
        lp_sd, lp_rho, lp_half = (float(x_) for x_ in P["low_pay"])
        lp_rng = np.random.default_rng([int(seed), 1723]); lp_z = np.zeros(N); lp_d = np.ones(N); lp_at = np.full(N, NEVER)
        lp_mu = np.zeros(N); lp_sc = np.ones(N)
        PC_ = P["pay_col"] if P.get("pay_col2") is None else P["pay_col2"]
        PC_ = None if PC_ is None else np.asarray(PC_, float)
    TC_ = None if P["tie_col"] is None else np.asarray(P["tie_col"], float)
    NET_ON = P["low_net"] is not None
    if NET_ON:
        net_y, net_lv, net_d = (tuple(float(x_) for x_ in P["low_net"]) + (1.0,))[:3]
        lo_w = np.zeros(N); net_ = np.zeros(N, bool); net_m = np.zeros(N); net_t = np.full(N, NEVER)
    PRP_ON = P["pair_pay"] is not None                    # F9.38: a couple living together shares its money
    if PRP_ON:
        CO_T_ = np.array([i_ for i_, x_ in enumerate(GR["names"]) if x_ in CO_TITLES], int) if RON else np.zeros(0, int)
    CRS_ON = bool(P["course"])                            # F16: the life course leans
    if CRS_ON:
        CRS_KS = np.array([PAR, KID, FAI]); CRS_MU = np.asarray(P["course_mu"], float)
        CRS_T = np.asarray(P["course_tilt"], float)
        crs_rng = np.random.default_rng([int(seed), 1605])
        crs_own = crs_rng.normal(0.0, P["course_sd"], (N, 3))   # each life's own lean
        # the life events that start one (falling in love, a baby on the way): most of their options start that kind
        sh_ = np.stack([((L["COMMIT"] == k_) & L["MASK"]).sum(1) for k_ in CRS_KS], 1) / np.maximum(L["MASK"].sum(1), 1)[:, None]
        ev_ok_ = (L["PERY"].sum(1) > 0)[:, None] & (sh_ >= 0.4)
        CRS_EV = np.where(ev_ok_.any(1), ev_ok_.argmax(1), -1)   # which of the three each situation starts (-1: none)
        CRS_J = np.full(NK, -1); CRS_J[CRS_KS] = np.arange(3)
        def course_q():
            """F16: each life's rate multiplier for starting a partnership, a child, a faith (N x 3)."""
            return np.exp(CRS_MU[None] + crs_own + (5 * w - 1) @ CRS_T.T)
    DC_ON = bool(P["deed_canon"])                         # F17: deeds by canon
    if DC_ON:
        DC_M = np.zeros((len(L["MARKS"]), C))
        for nm_, v_ in DEED_CANON.items():
            if nm_ in L["MARKS"]:
                DC_M[L["MARKS"].index(nm_)] = v_
        DC_L = np.where((L["MARK"] >= 0)[..., None], DC_M[np.maximum(L["MARK"], 0)], 0.0)   # S x K x C: each option's lean
    DR_ON = bool(P["deed_rare"])
    if DR_ON:
        DR_M = np.isin(np.arange(len(L["MARKS"])), [L["MARKS"].index(m_) for m_ in DEED_RARE if m_ in L["MARKS"]])
        dr_rng = np.random.default_rng([int(seed), 1705])
    # spheres finishing pack, part 4: former inmates as ties (finish-pack-draft.md; sphere_data.DEEP service.after_prison.
    # tie_values). A release is the week a known term ends (pris_out) or the week [ex-prisoner] comes by its rule with no
    # term pending. Every release is kept (yrs_out; nothing is drawn); the ties come only with prison_ties and the world
    # on (People holds them; never for a life under 18, and each fellow inmate is an adult). Its own draws: pt_rng
    EXP_I = int(GR["ID"].get("ex-prisoner", -1)) if RON else -1
    pt_rel = np.full(N, NEVER); pt_seen = np.full(N, NEVER)   # the last release; the [ex-prisoner] gain last read
    pt_act = np.zeros(N, bool)                                # an active former-inmate tie (inmate_tie)
    PT_ON = bool(P.get("prison_ties")) and WON and RON and getattr(WL.PP, "inmate", None) is not None
    pt_log = []                                               # the readout: made and ended ties
    PT_TEST = (P.get("prison_par") or {}).get("test")         # checks only: (age, years) every life serves a term
    if PT_ON:
        import sphere_data as SD_, world_keys as WK_, world_people as PM_
        TV_ = SD_.DEEP["service"]["after_prison"]["tie_values"]; PTP_ = {**DEFAULT["prison_par"], **(P.get("prison_par") or {})}
        PT_Y = tuple(float(x_) for x_ in TV_["made_y"]); PT_C0 = float(TV_["strength"]); PT_YRS = int(52 * TV_["years"])
        PT_PULL = float(TV_["pull_back"]["reoffend"] if PTP_["pull"] is None else PTP_["pull"])   # odds x this (pt_pull_u)
        PT_HELP = TV_["help"]; PT_STM = float(PT_HELP["stress_m"])
        PT_D = -np.log(float(PT_HELP["hiring"])) / 3              # hiring odds x 1.1 as difficulty (odds x exp(-3 x d))
        se_ = np.asarray(GR["sector"]) if "sector" in GR else np.full(NT_, -1)
        PT_SEC = np.array([0 <= int(se_[i_]) < len(WK_.SECTORS) and WK_.SECTORS[int(se_[i_])] in PT_HELP["sectors"]
                           for i_ in range(NT_)] + [False], bool)   # a title's work in farm or industry (-1: no title)
        PT_JOB = np.nonzero(np.asarray(TK_[:NT_]) == CAR)[0]       # the job titles (steady work: one held a year or more)
        PT_BL = (L["MARK"] == L["MARKS"].index("broke the law")) if "broke the law" in L["MARKS"] else np.zeros_like(L["MARK"], bool)
        pt_n = np.zeros(0, np.int64); pt_k = np.zeros(0, np.int64); pt_u = np.zeros(0, np.int64); pt_t = np.zeros(0, np.int64)
        pt_pull = np.zeros(N, bool)
        pt_rng = np.random.default_rng([int(seed), 2404])

        def pt_release(ns_, known_):
            """Part 4: lives ns_ released this week make ties with fellow inmates: years inside (the term, else
            years_unknown) x uniform(made_y) a year, rounded, at most cap; adults near their age, of their sex (prisons
            hold men and women apart), at the data's strength, in their People as friends, marked inmate."""
            nonlocal pt_n, pt_k, pt_u, pt_t
            PP_ = WL.PP
            if age < 18:   # never a child
                return
            yrs_ = np.where(known_ & (pris_in[ns_] > NEVER), (t - pris_in[ns_]) / 52.0, float(PTP_["years_unknown"]))
            m_ = np.minimum(np.round(yrs_ * pt_rng.uniform(*PT_Y, len(ns_))).astype(np.int64), int(PTP_["cap"]))
            nn_ = np.repeat(ns_, m_)
            if not len(nn_):
                return
            ag_ = np.maximum(18.0, age + pt_rng.normal(0, 5, len(nn_)))
            rng0_ = PP_.rng; PP_.rng = pt_rng   # People's own draws for these people come from the part's stream
            try:
                F_ = PP_._gen(nn_, PP_.t - (ag_ * 52).astype(np.int64), PP_.t)
                F_["fem"] = female[nn_].copy()
                sl_ = PP_._add(F_, PP_.t, PM_.R["friend"], c0=PT_C0, trust0=0.5, acc0=0.1, quiet=True)
            finally:
                PP_.rng = rng0_
            ok_ = sl_ >= 0; nn_, sl_ = nn_[ok_], sl_[ok_]
            PP_.inmate[nn_, sl_] = True; PP_.inmate_t[nn_, sl_] = PP_.t
            uu_ = PP_.uid[nn_, sl_].astype(np.int64)
            pt_n = np.concatenate([pt_n, nn_]); pt_k = np.concatenate([pt_k, sl_]); pt_u = np.concatenate([pt_u, uu_])
            pt_t = np.concatenate([pt_t, np.full(len(nn_), t)])
            pt_log.extend(dict(n=int(n_), t=int(t), other=int(u_), what="made", why="met inside")
                          for n_, u_ in zip(nn_.tolist(), uu_.tolist()))

        def pt_week():
            """Part 4, each week: the ties still active (living, still in their People, closeness at or above active,
            within the 10 years); the ended leave the readout and fade at the usual speed again."""
            nonlocal pt_n, pt_k, pt_u, pt_t, pt_act
            PP_ = WL.PP
            if not len(pt_n):
                pt_act = np.zeros(N, bool)
                return
            here_ = PP_.used[pt_n, pt_k] & (PP_.uid[pt_n, pt_k] == pt_u)
            live_ = here_ & PP_.lv[pt_n, pt_k]
            why_ = np.where(dead[pt_n], 4, np.where(~here_, 2, np.where(~live_, 1, np.where(t - pt_t >= PT_YRS, 3,
                            np.where(PP_.c[pt_n, pt_k] < PTP_["active"], 0, -1)))))
            end_ = why_ >= 0
            if end_.any():
                WHY_ = ("faded", "died", "gone", "ten years", "life ended")
                pt_log.extend(dict(n=int(n_), t=int(t), other=int(u_), what="ended", why=WHY_[w_])
                              for n_, u_, w_ in zip(pt_n[end_].tolist(), pt_u[end_].tolist(), why_[end_].tolist()))
                hk_ = end_ & here_
                PP_.inmate[pt_n[hk_], pt_k[hk_]] = False
                keep_ = ~end_; pt_n, pt_k, pt_u, pt_t = pt_n[keep_], pt_k[keep_], pt_u[keep_], pt_t[keep_]
            pt_act = np.zeros(N, bool); pt_act[pt_n] = True
    if P["mind_kid"] is not None:                         # F19
        MK_A, MK_F = np.asarray(P["mind_kid"], float).T
    if P["mind_u"] is not None:
        MU_A, MU_F = np.asarray(P["mind_u"], float).T
    # the world's effects on each life, for the game's story (stage 1: WL1, WL3, WL5): only in a game run (pausing) with
    # the world on, and read only, so every life is the same with them or without
    WFX_ON = bool(pausing and WON)
    wfx = [[] for _ in range(N)]                         # this week's world effects on each life (wfx_add)
    wfx_last = {}                                         # (channel, kind) -> the value last reported, per life (N,)
    wco_ = {}                                             # this week's option closures by cause (option_causes)

    def wfx_add(n, kind, channel, size, age_, cause=None, **more):
        """An effect of the world on life n: kind (the world's cause: prices, housing, welfare, rights, crime, war,
        disaster, unemployment, illness, pandemic, or a world event's kind), channel (what of theirs it touched),
        size (signed, in the channel's units), dir (up or down), cause (the world's record entry behind it, for the
        hover; None when the record has none), age; more keys as given (moment, share, hazard)."""
        e_ = dict(kind=kind, channel=channel, size=round(float(size), 4), dir="up" if size > 0 else "down",
                  cause=cause if cause is not None else WL.cause(kind), age=round(float(age_), 2))
        e_.update(more)
        wfx[n].append(e_)

    def wfx_track(channel, parts, age_, dead_):
        """Report each part (kind -> (N,)) that moved by wfx_step or more since it was last reported; the first
        reading only sets where it starts."""
        for kd_, v_ in parts.items():
            v_ = np.broadcast_to(np.asarray(v_, float), (N,))
            old_ = wfx_last.get((channel, kd_))
            if old_ is None:
                wfx_last[(channel, kd_)] = v_.copy()
                continue
            mv_ = np.nonzero(np.abs(v_ - old_) >= P["wfx_step"])[0]
            for n_ in mv_:
                if not dead_[n_]:
                    wfx_add(n_, kd_, channel, v_[n_] - old_[n_], age_)
            old_[mv_] = v_[mv_]

    def option_causes(n):
        """The world's causes behind each option of life n's moment this week (WL3), one list per option, each cause a
        dict: kind (law, norm, role, technology, unemployment, university places, hospital places), key (the law,
        norm or technology), channel "option", size (law: 1 banned, .5 restricted, -1 allowed where written closed;
        norm, role, technology: closure units; unemployment and places: difficulty added, - easier), how, cause (the
        world's record entry, as in wfx). Empty without the world or before the first moment."""
        if not wco_:
            return []
        s_ = int(wco_["s"][n]); K_ = len(L["labels"][s_]); out = [[] for _ in range(K_)]
        WK_ = WLM.WK; lw_, nm_, te_ = WL.law[s_], WL.norm[s_], WL.tech[s_]
        def add(k_, kind, key, size, how):
            out[k_].append(dict(kind=kind, key=key, channel="option", size=round(float(size), 4), how=how,
                                cause=WL.cause(kind, key=key if kind in ("law", "technology") else None)))
        od_ = WL.odds_parts(wco_["s"])
        for k_ in range(K_):
            if k_ < lw_.shape[0] and lw_[k_] >= 0:
                u_ = float(wco_["ul"][n, k_])
                if u_ > 0:
                    add(k_, "law", WK_.LAW_KEYS_ALL[lw_[k_]], u_, "banned" if u_ >= 1 else "restricted")
                elif wco_["lo"][n, k_] and wco_["closed0"][n, k_] == 0:
                    add(k_, "law", WK_.LAW_KEYS_ALL[lw_[k_]], -1.0, "allowed")
            if k_ < nm_.shape[0] and nm_[k_] >= 0 and wco_["ua"][n, k_] >= WFX_OPT[0]:
                add(k_, "norm", WK_.NORM_KEYS_ALL[nm_[k_]], wco_["ua"][n, k_], "frowned on")
            if wco_.get("role") is not None and wco_["role"][n, k_] >= WFX_OPT[0]:
                add(k_, "role", "role crossing", wco_["role"][n, k_], "frowned on")
            if k_ < te_.shape[0] and te_[k_] >= 0:
                if wco_["gone"][n, k_]:
                    add(k_, "technology", WK_.TECH_KEYS[te_[k_]], 1.0, "not there")
                elif wco_["um"][n, k_] >= WFX_OPT[0]:
                    add(k_, "technology", WK_.TECH_KEYS[te_[k_]], wco_["um"][n, k_], "out of reach")
            for kd_, v_ in od_.items():
                v_ = np.broadcast_to(v_, (N, WL.job_o.shape[1]))   # a moment-wide part (an illness's) is (N, 1)
                if abs(v_[n, k_]) >= WFX_OPT[1]:
                    add(k_, kd_, None, v_[n, k_], "harder" if v_[n, k_] > 0 else "easier")
        return out
    def _handed():   # never called: naming the handed-over variables here (STATE, STATE_IF, STATE_MORE) makes each a
        # cell, so a pause reads them one by one (locals() copies all ~1,600 of the run's variables, 1 ms a pause)
        return (P, L, t, age, RON, AQ_ON, SEA_ON, TH_K, TH_STEP, TH_TR, AT0, RS0, WL, z, w, y, k, M, sig, SE,
                fb, habit, hold, nic, res, need, doors, f_tot, B, X, mood, content, peace, stress, react,
                steady, base_mood, outlook, plast, ctrl, dsc, support, wound, trouble, fortune, Q, q_thr, TWo,
                fhz, hzf, gap_r, regret, earned, held, I, prof, sat, since, stage, alive, dead, died, widowed,
                female, intersex, found_id, faith_given, faith_drifted, clash0, act_cw, rfit_avg, adj,
                adj_since, adj_v, mark_n, had_ev, missed_t, events, tries, wins, blocked, sit_n, sea_k, sea_t0,
                sea_done, gk, gm, gd, gs, gp, gh, ghz, gsrc, gby, gid, gname, gfelt, gfelt0, gplay, new_goal,
                end_goal, quit_, plan_odds, dream_phrase, s, s_ev, rk, recon, m, e, e0, diff, mask, closed_s,
                stakes, alpha, do_nothing, lack, lackf, earn, pbump, serves, relief, rel, wR, gU_R, gU_I, w_hat,
                a_hat, V, VA, H, hzU, step, tryf, U_R, U_I, U, read_, readk_, open_r, open_, seen, pr, p_hat, a,
                ma, ea, ph, idle, p_true, succ, delta, span, stepF, role, pr0, steer_moved, shS, shA, sh_src,
                sh_seen, SHON, asked, CU_ON, NMP, NM_ON, cur_sum, cur_m, CUR_ON, body_v, mind_v, md_end, dl_at,
                dl_t0, dl_cause, bd_cw, bd_ck, bd_sk, HM_ON, DTH_ON, settle_f, e_i, e_p, wfx, option_causes,
                ev_log, goal_log, brk_log, conv_log, rite_log, commit_log, clash_log, role_log, adj_log,
                mark_log, read_log, r_has, r_ever, r_since, r_prof, p_acc, p_lev, p_sus, fam, gsr, goal_rel_S,
                around, retired, ck, ok_, frc_, ONCE_HOLD_, noise, btrust, ep_seeds, ep_now, asrc, asrc_c,
                bold_now, bold_pick)
    if pausing:
        ST_CELLS = tuple(zip(_handed.__code__.co_freevars, _handed.__closure__)); ST_FR = sys._getframe()
        pz_st = PauseState()
