# run_06_world.py: part 6 of 18 of engine._run, the life loop.
# The outer world (WorldLink), service, debts, household and ties, the F switches.
# Lines here are _run's own, unchanged and at their own indent: engine.py joins the parts in order (engine.RUN_PARTS)
# and compiles them as one, so a name used here may be set in an earlier part. Never import or run it alone.
    if WON:
        import world_link as WLM
        WL = WLM.WorldLink(sys.modules[__name__], P, L, N, seed, female, attr, KILLS, ENDS, CAR)
        WL.PP.or_on = bool(P.get("one_roll"))   # F7: a partner the world takes is not replaced (world_people._sync)
        if P["work_die"] is not None:   # F9.29: a death at work, a work-year at this x danger (world_people._marks_year)
            WL.PP.mk_die = float(P["work_die"])
        LW_ON = bool(getattr(WL, "lw", False)) and RON
        if LW_ON:
            LW_T_ = WL.lw_tid
        nic = np.array(WL.PP.niche, float); circle = nic.copy()
        STH_ON = bool(P.get("start_hold"))
        if STH_ON and (getattr(WL, "start", None) or {}).get("society") is not None:   # the start's society around them
            STH_SOC = np.asarray(WL.start["society"], float); STH_SOC = STH_SOC / STH_SOC.sum()
            STH_FW = np.asarray(P["f_world"], float)
            nic = (1 - P["start_soc"]) * nic + P["start_soc"] * STH_SOC; circle = nic.copy()
        SOC_OWN = float(P["soc_own"] or 0.0); onic = nic.copy() if SOC_OWN else None
        SEEN_ON = bool(P.get("seen_done")) and WL.seen_on   # S6, seen it done: felt odds and young dreams (world_people)
        if SEEN_ON:
            SD_DREAM_ = float(WL.PP.sd_par["dream"]); SD_AGES_ = tuple(WL.PP.sd_par["dream_ages"])
        BT_ON = bool(P.get("body_trust")) and bool(getattr(WL.PP, "bt_on", False))   # finishing pack part 3 (world_people)
        if BT_ON:
            import sphere_data as SD_
            btrust = WL.PP.btrust                          # the People's own array (N x 9, NaN before 15), updated in place
            BTJ_ = SD_.TRUST["jumps"]; BT_G = SD_.TRUST["gate"]
            BT_CARE_J = WLM.WK.SPHERES.index("care"); BT_PROT_J = WLM.WK.SPHERES.index("prot"); BT_RULE_J = WLM.WK.SPHERES.index("rule")
            # an own run-in with a body (finish-pack-draft.md: an unjust verdict, a cure that failed, a heavy hand; a fair
            # hearing, a cure, help from the watch): a moment set at a body (at:) in that body's sphere, else an illness's
            # moment in care and a crime's in prot; its act working is the run-in going well, failing going against them
            at_ = np.asarray(L.get("W_AT", np.full(L["S"], -1)))[:L["S"]]
            BT_RUN = np.where(at_ >= 0, WLM.PM.BT_INST_J[np.maximum(at_, 0)], -1)
            BT_RUN = np.where((BT_RUN < 0) & WL.ill_s, BT_CARE_J, BT_RUN)
            BT_RUN = np.where((BT_RUN < 0) & (WL.rk == WLM.RK.index("crime")), BT_PROT_J, BT_RUN)
            bt_y = np.full((N, years, len(WLM.WK.SPHERES)), np.nan)   # each life's trust at the end of each year of age
            if RON:   # the body kind each title is held at (its institution's, or the force's by name; -1 none)
                _bins = np.asarray(GR.get("institution", np.full(NT_, -1)))[:NT_]
                BT_TK = np.array([WLM.PM.bt_title_kind(GR["names"][i_], _bins[i_]) for i_ in range(NT_)], np.int64)
                BT_TI = np.nonzero(BT_TK >= 0)[0]
        if getattr(WL.PP, "family_mix", None) is not None:
            fam = np.array(WL.PP.family_mix, float)
        older_sib = np.asarray(WL.PP.older_sib, int).copy(); younger_sib = np.asarray(WL.PP.younger_sib, int).copy()
        alive[:, :5] = WL.PP.alive
        era_at.clear()                                     # the world's own eras replace the engine's drawn history
        W_WHO_ = L.get("W_WHO", [[] for _ in range(L["S"])])
        SAC_ON_ = bool(getattr(WL.PP, "sac_on", False))   # S5: the world's switch (P["sacred"], or a World made with it)
        if RON:
            W_SEC_ = np.asarray(GR.get("sector", np.full(NT_, -1)))[:NT_]; W_STD_ = np.asarray(GR.get("standing", np.full(NT_, -1)))[:NT_]
            W_GOV_ = [RID[x_] for x_ in ("minister", "head of government") if x_ in RID]; W_HOG_ = RID.get("head of government", -1)
            W_SDI_ = np.nonzero(W_STD_ >= 0)[0]   # titles with a standing, and the domain each counts in (spec 7 §2)
            _ins = np.asarray(GR.get("institution", np.full(NT_, -1)))[:NT_]; _sec = W_SEC_
            W_SDOM_ = np.array([WLM.WK.DOMAINS.index(WLM.title_domain(GR["names"][i_], WLM.WK.INST_KINDS[_ins[i_]] if _ins[i_] >= 0 else None,
                                                                     WLM.WK.SECTORS[_sec[i_]] if _sec[i_] >= 0 else None)) for i_ in W_SDI_], int)
        KCHILD_ = KILLS == ROLES.index("child")
        dq_ = np.zeros((N, 5), bool); dq_t = np.zeros((N, 5), np.int64)   # a cast death waiting for its moment (role, since)
        clim_w = np.zeros(N); DIS_J_ = [j_ for j_, e_ in enumerate(EVR) if WLM.DIS_EVR.search(e_["name"])]
        evr_ok = np.zeros((N, len(EVR)))   # a disaster's outside event comes again only after its shortest gap

        def world_cast(lst_):   # the cast's events in the story: a push is reported once (world_push), and a want the
            for e_ in lst_:     # moment met or refused once (cast_want)
                if e_.get("n") in events and e_.get("kind") != "push" and not (e_.get("kind") == "want" and "worked" in e_):
                    events[e_["n"]].append(dict(cast=e_))
        # WL6, for P["dis_match"] (the game may turn it on mid-run): the hazards each disaster event fits (by name); one
        # naming no hazard fits them all
        hz_j_ = {j_: {h_ for h_, rx_ in WLM.HAZ_EVR.items() if re.search(rx_, EVR[j_]["name"], re.I)} for j_ in DIS_J_}
        DIS_FOR_ = {}
        for h_ in WLM.HAZ_EVR:
            own_j_ = [j_ for j_ in DIS_J_ if h_ in hz_j_[j_]]; any_j_ = [j_ for j_ in DIS_J_ if not hz_j_[j_]]
            DIS_FOR_[h_] = set(own_j_ or any_j_ or DIS_J_)
    SV_ON = bool(P.get("sph_deep")) and WON and RON  # spheres phase 5: service as a chapter (deep_state.service)
    if SV_ON:
        import sphere_data as SD_, world_keys as WK_
        SVC_T = np.array([RID[x_] for x_ in ("soldier", "police officer") if x_ in RID], int)   # the host, the guard
        PROT_N = {"soldier", "police officer", "firefighter", "security guard"}
        def t_sph_(i_):   # a title's sphere: by name for the force, else its institution's, else its sector's
            if GR["names"][i_] in PROT_N:
                return "prot"
            in_ = int(GR["institution"][i_]) if "institution" in GR else -1
            if in_ >= 0 and WK_.INST_SPHERE[WK_.INST_KINDS[in_]]:
                return WK_.INST_SPHERE[WK_.INST_KINDS[in_]]
            se_ = int(GR["sector"][i_]) if "sector" in GR else -1
            return WK_.SECTOR_SPHERE[WK_.SECTORS[se_]] if se_ >= 0 else None
        PR_T = np.array([t_sph_(i_) in ("prot", "rule") for i_ in range(NT_)] + [False], bool)   # (-1: no title)
        SVS_ = SD_.DEEP["service"]; HV_ = SVS_["after_guard_or_host"]["hiring"]
        RW_ = float(SD_.DEEP["record_weight"].get(getattr(WL.W, "sph_epoch", "modern"), 1.0))
        # hiring odds as the options' difficulty (DIFF units: odds x exp(-3 x d))
        SV_D = (-np.log(1 + HV_["prot"]) / 3, -np.log(1 + HV_["other"]) / 3, -np.log(1 - 0.5 * RW_) / 3)
        # debts and holdings (deep_state.debts, holdings, money_map): a ledger of up to four debts and two holdings per
        # life, on the engine's money: a year's income is mt, a month's mt / 12 (spheres-phase5b-asks.md)
        DBT_ = SD_.DEEP["debts"]["holders"]; MM_ = SD_.DEEP["money"]; HKS_ = SD_.DEEP["holdings"]["kinds"]; DP_ = P["deep_par"]
        D_KIND = ["tab", "kin", "circle", "bank", "lender", "home_loan"]
        D_RATE = np.array([float(DBT_[k_]["rate"]) for k_ in D_KIND[:5]] + [0.04])
        D_SIZE = np.array([float(DBT_[k_]["size_months"]) for k_ in D_KIND[:5]] + [0.0])
        D_TERM = np.array([float(MM_["term_months"][k_]) for k_ in D_KIND])
        LSF_TERM = float(MM_["term_months"].get("land_shop_firm_loan", 120.0))   # land, a shop or a firm on a bank loan
        LT_I = next((i_ for i_, e_ in enumerate(SD_.EV) if e_["key"] == "land_taken"), -1)   # prod.land_taken
        WL.PP.care_buy_x = float(DP_["care_buy"][1])
        ep_ = getattr(WL.W, "sph_epoch", "modern")
        EPI_ = SD_.EPOCHS.index("sail" if ep_ == "magic" else ep_)   # magic: as sail, its base
        D_FROM = np.array([SD_.EPOCHS.index(DBT_[k_]["from"]) for k_ in D_KIND[:5]] + [SD_.EPOCHS.index("sail")])
        D_LEND = EPI_ >= D_FROM                              # which holders lend in this world's epoch
        H_KIND = ["home", "land_boat_herd", "workshop_shop", "firm"]
        H_VAL = np.array([float(HKS_[k_]["value_years"]) for k_ in H_KIND])
        H_YV = H_VAL * np.array([float(HKS_[k_]["yield"]) for k_ in H_KIND])   # a year's yield in years of income
        H_OK = EPI_ >= np.array([1, 1, 1, SD_.EPOCHS.index(HKS_["firm"].get("from", "sail"))])   # bands: no holdings
        NL_ = float(MM_["need_line"]); YR_ = 52; ER_ = ep_ if ep_ != "magic" else "sail"
        DL_ = int(SD_.DEEP["debts"]["ledger"])
        dk = np.full((N, DL_), -1); dsz = np.zeros((N, DL_)); dbal = np.zeros((N, DL_)); dpaid = np.zeros((N, DL_), int)
        dterm = np.ones((N, DL_)); drate = np.zeros((N, DL_)); dhold = np.full((N, DL_), -1)   # the holding a loan bought
        dstr = np.zeros((N, DL_), bool)                      # a kin debt stretched once by another term
        ev_seen = [0]                                        # the sphere events read so far (a land taking)
        hk = np.full((N, int(SD_.DEEP["holdings"]["max"])), -1)
        tab_shut = np.full(N, NEVER); kin_shut = np.full(N, NEVER); circ_out = np.zeros(N, bool); brec = np.full(N, NEVER)
        d_inc = np.full(N, float(P["money_base"]))           # a year's income, mt before holdings and payments
        car_prev = np.zeros(N, bool); hea_prev = np.ones(N); rec_prev = [False]
        hs_rng = np.random.default_rng([int(seed), 1719])   # F9.15 home_sale, on its own stream
        d_arm = np.ones(N, bool)   # a fall under the need line borrows once; again after climbing back or a new blow
        db_rng = np.random.default_rng([int(seed), 82])     # the debts' and holdings' draws, on their own stream
        DB_D = -np.log(1 - 0.05) / 3                         # a bank's record: hiring odds x .95 for 7 years

        def db_log(n, **kw):
            if n in events:
                events[n].append(dict(deep_state=dict(kw, age=round(t / 52, 2))))

        def db_clear(n, i):
            dk[n, i] = -1; dsz[n, i] = dbal[n, i] = 0.0; dpaid[n, i] = 0; dterm[n, i] = 1.0; drate[n, i] = 0.0; dhold[n, i] = -1
            dstr[n, i] = False

        def db_add(n, kind, size, term, rate, hold=-1):
            i = int(np.argmax(dk[n] < 0))
            dk[n, i] = kind; dsz[n, i] = dbal[n, i] = size; dpaid[n, i] = 0; dterm[n, i] = term; drate[n, i] = rate
            dhold[n, i] = hold
            db_log(n, kind="debt taken", holder=D_KIND[kind], months=round(float(size), 2))

        def db_share(n):   # the part of income the payments take
            a_ = dk[n] >= 0
            return float((dsz[n] / dterm[n] + drate[n] * dbal[n] / 12)[a_].sum())

        def bank_ok(n):    # a bank lends: the world's epoch, the town's credit and the person's class, no record
            if not D_LEND[3] or (brec[n] > NEVER and t - brec[n] < 7 * YR_):
                return False
            cr_ = float(WL.W.sph_state("comm.credit")[WL.PP.loc[n]])
            return cr_ + DP_["bank_cls"] * (int(WL.PP.cls[n]) - 1) >= DP_["bank_line"]

        def db_break(n, i):   # a debt that cannot be paid breaks (deep_state.debts.broken), by holder
            k_ = int(dk[n, i]); h_ = int(dhold[n, i])
            if k_ == 1:
                WL.PP.kin_let_down(n, DP_["kin_trust"], t); kin_shut[n] = t + DP_["kin_wait"] * YR_
            elif k_ == 0:
                tab_shut[n] = t + DP_["tab_wait"] * YR_
            elif k_ == 2:
                circ_out[n] = True
            elif k_ in (3, 5):
                brec[n] = t
            elif k_ == 4:   # the debt is sold on and pressed: a threat, read by the town's order (never graphic)
                od_ = float(WL.W.sph_state("prot.order")[WL.PP.loc[n]])
                stress[n] += DP_["lender"][0] + DP_["lender"][1] * (1 - od_)
            db_log(n, kind="debt broken", holder=D_KIND[k_])
            db_clear(n, i)
            if h_ >= 0 and hk[n, h_] >= 0:   # the holding the loan bought goes with it
                db_log(n, kind="holding lost", holding=H_KIND[int(hk[n, h_])], why="debt")
                hk[n, h_] = -1

        def db_month():
            """Each month (adults): a hard year makes the nearest debt due, payments run down the balances, a debt that
            ends unpaid breaks, a life under the need line borrows; once a year, a holding may be bought."""
            m1_ = np.maximum(d_inc, 0.02) / 12               # a month's income on the money level
            car_ = held[:, CAR].copy(); hea_ = res[:, HEA].copy(); rec_ = getattr(WL.W, "phase", 0) == 1
            hard_ = ~dead & ((car_prev & ~car_ & (age < 60)) | (rec_ and not rec_prev[0])
                             | ((hea_ < DP_["ill_line"]) & (hea_prev >= DP_["ill_line"])))
            car_prev[:] = car_; hea_prev[:] = hea_; rec_prev[0] = rec_
            d_arm[:] |= (res[:, MON] >= NL_) | hard_
            for n in np.nonzero(hard_)[0]:
                if res[n, MON] < NL_ and (hk[n] >= 0).any():   # a sale in a hard year: a holding other than the home first
                    j_ = int(np.argmax(np.where(hk[n] >= 0, np.where(hk[n] == 0, 1, 2), 0)))
                    if hk[n, j_] == 0 and P["home_sale"] < 1.0 and hs_rng.random() >= P["home_sale"]:
                        j_ = -1                                 # F9.15: they get by without selling the home
                if res[n, MON] < NL_ and (hk[n] >= 0).any() and j_ >= 0:
                    res[n, MON] = min(1.0, res[n, MON] + DP_["sale"] * H_VAL[hk[n, j_]] * 12 * m1_[n])
                    for i_ in np.nonzero(dhold[n] == j_)[0]:
                        res[n, MON] = max(0.0, res[n, MON] - dbal[n, i_] * m1_[n]); db_clear(n, i_)
                    db_log(n, kind="holding lost", holding=H_KIND[int(hk[n, j_])], why="sold"); hk[n, j_] = -1
                rows_ = np.nonzero((dk[n] >= 0) & (dk[n] != 5))[0]   # the nearest due debt is due now (a home loan runs on)
                if len(rows_):
                    i_ = int(rows_[np.argmin((dterm[n] - dpaid[n])[rows_])])
                    if res[n, MON] < NL_:
                        db_break(n, i_)
                    else:
                        res[n, MON] -= dbal[n, i_] * m1_[n]; db_log(n, kind="debt paid early", holder=D_KIND[int(dk[n, i_])])
                        db_clear(n, i_)
            act_ = (dk >= 0) & ~dead[:, None]
            dpaid[act_] += 1; dbal[act_] = np.maximum(0.0, dbal[act_] - (dsz / dterm)[act_])
            for n, i_ in zip(*np.nonzero(act_ & (dpaid >= dterm))):
                if res[n, MON] >= 0.1 or (P["loan_end"] and dk[n, i_] == 5):   # F9.15: a home loan at its term is paid
                    db_clear(n, i_)
                elif dk[n, i_] == 1 and not dstr[n, i_]:   # kin: a partner or parent forgives it, else it is stretched once
                    al_ = WL.PP.alive[n]
                    if (al_[0] > 0 or al_[4] > 0) and db_rng.random() < DP_["kin_forgive"]:
                        db_log(n, kind="debt forgiven", holder="kin"); db_clear(n, i_)
                    else:
                        dstr[n, i_] = True; dpaid[n, i_] = 0; dsz[n, i_] = dbal[n, i_] = 0.5 * dsz[n, i_]
                        db_log(n, kind="debt stretched", holder="kin")
                else:
                    db_break(n, i_)
            for n in np.nonzero(~dead & d_arm & (res[:, MON] < NL_) & (dk < 0).any(1))[0]:   # borrowing, in the lending order
                gap_ = (NL_ - res[n, MON]) / m1_[n]
                run_ = set(int(x_) for x_ in dk[n] if x_ >= 0)
                al_ = WL.PP.alive[n]
                if gap_ < 0.5 and D_LEND[0] and tab_shut[n] <= t and 0 not in run_:
                    k_ = 0
                elif D_LEND[1] and kin_shut[n] <= t and 1 not in run_ and al_[0] + al_[1] > 0:
                    k_ = 1
                elif D_LEND[2] and not circ_out[n] and 2 not in run_:
                    k_ = 2
                elif 3 not in run_ and bank_ok(n):
                    k_ = 3
                elif D_LEND[4] and 4 not in run_:
                    k_ = 4
                else:
                    continue
                db_add(n, k_, D_SIZE[k_], D_TERM[k_], D_RATE[k_]); d_arm[n] = False
                res[n, MON] = min(1.0, res[n, MON] + D_SIZE[k_] * m1_[n])
            if t % YR_ == 0 and 25 <= age <= 65 and H_OK[0]:   # buying, a home first, then land, a shop or a firm, by the
                # lines on the life's own income (phase5c-answers.md): with a bank from sail on, from savings before
                u_ = db_rng.random(N)
                for n in np.nonzero(~dead & (hk < 0).any(1))[0]:
                    j_ = int(np.argmax(hk[n] < 0)); free_ = (dk[n] < 0).any(); mt_ = float(d_inc[n]); lv_ = float(res[n, MON])
                    home_ = not (hk[n] == 0).any()
                    if D_LEND[3]:   # banks lend in this epoch
                        a_, b_, p_ = DP_["buy_home"] if home_ else DP_["buy_more"]
                        if not (u_[n] < p_ and mt_ >= a_ and lv_ >= b_ * mt_ and free_ and bank_ok(n)):
                            continue
                        if home_:
                            k_ = 0; loan_ = max(0.0, H_VAL[0] * 12 - 0.1 / m1_[n]); term_, rate_, kd_ = D_TERM[5], D_RATE[5], 5
                        else:
                            ks_ = [x_ for x_ in (1, 2, 3) if H_OK[x_]]
                            k_ = ks_[int(db_rng.integers(len(ks_)))]
                            loan_ = (H_VAL[k_] - 1) * 12; term_, rate_, kd_ = LSF_TERM, D_RATE[3], 3   # above one year
                        if db_share(n) + loan_ / term_ + rate_ * loan_ / 12 > DP_["max_share"]:
                            continue
                        res[n, MON] = max(0.1, lv_ - (0.1 if home_ else 12 * m1_[n]))   # the deposit, or one year's income
                        hk[n, j_] = k_; db_add(n, kd_, loan_, term_, rate_, hold=j_)
                    else:           # before banks: from savings
                        a_, b_, p_ = DP_["buy_nb_home"] if home_ else DP_["buy_nb_more"]
                        if not (u_[n] < p_ and lv_ >= a_ and mt_ >= b_):
                            continue
                        ks_ = [0] if home_ else [x_ for x_ in (1, 2, 3) if H_OK[x_]]
                        k_ = ks_[int(db_rng.integers(len(ks_)))]
                        res[n, MON] = max(0.1, lv_ - 12 * m1_[n]); hk[n, j_] = k_
                    db_log(n, kind="holding gained", holding=H_KIND[k_], why="bought")
            # a land taking in the life's town (prod.land_taken) takes held land
            lg_ = getattr(WL.W, "sph_ev_log", None)
            if lg_ is not None and len(lg_) > ev_seen[0]:
                new_ = lg_[ev_seen[0]:]; ev_seen[0] = len(lg_)
                for _, e_, l_ in new_[new_[:, 1] == LT_I] if LT_I >= 0 else ():
                    for n in np.nonzero(~dead & (hk == 1).any(1) & ((WL.PP.loc == l_) | (l_ < 0)))[0]:
                        if db_rng.random() < DP_["land_taken"]:
                            j_ = int(np.argmax(hk[n] == 1)); hk[n, j_] = -1
                            for i_ in np.nonzero(dhold[n] == j_)[0]:
                                db_clear(n, i_)
                            db_log(n, kind="holding lost", holding=H_KIND[1], why="taken")
            if getattr(WL.PP, "care_buy", None) is not None:   # a carer with money buys help: care hours x .7
                WL.PP.care_buy[:] = res[:, MON] >= DP_["care_buy"][0]
            WL.PP.roots[:] = (hk >= 0).any(1)                # roots: the move wish x .5 while one is held

        def db_inherit(n):
            """The last living parent dies: what the family held passes by the epoch's rule (deep_state.holdings.
            inheritance), the life's share 1 / (1 + siblings), a daughter's share x rights['women']."""
            cl_ = int(WL.PP.cls_home[n]); nsib_ = int(WL.PP.older_sib[n] + WL.PP.younger_sib[n])
            eld_ = int(WL.PP.older_sib[n]) == 0
            sh_ = 1.0 / (1 + nsib_)
            if female[n]:
                sh_ *= float(np.asarray(WL.W.rights)[WK_RIGHTS_W])
            est_ = []
            if db_rng.random() < DP_["estate_home"][0] + DP_["estate_home"][1] * cl_:
                est_.append(0)
            if db_rng.random() < DP_["estate_more"][0] + DP_["estate_more"][1] * cl_:
                ks_ = [k_ for k_ in (1, 2, 3) if H_OK[k_] and (k_ < 3 or cl_ == 2)]
                est_.append(ks_[int(db_rng.integers(len(ks_)))])
            m_ = max(float(d_inc[n]), 0.02)
            for k_ in est_:
                s_ = sh_
                if (k_ == 1 and ER_ in ("realms", "sail")) or (k_ == 0 and ER_ == "cities"):   # to the eldest
                    s_ = (1.0 if eld_ else 0.0) * (float(np.asarray(WL.W.rights)[WK_RIGHTS_W]) if female[n] else 1.0)
                if s_ <= 0:
                    continue
                if s_ >= 0.5 and (hk[n] < 0).any() and not (hk[n] == k_).any():
                    hk[n, int(np.argmax(hk[n] < 0))] = k_
                    db_log(n, kind="holding gained", holding=H_KIND[k_], why="inherited")
                else:   # a share in money: s x value years of income
                    res[n, MON] = min(1.0, res[n, MON] + s_ * H_VAL[k_] * m_)
                    db_log(n, kind="inheritance", holding=H_KIND[k_], share=round(s_, 2))
        import world as WMOD_
        WK_RIGHTS_W = WMOD_.RIGHTS.index("women")
    DB_ON = SV_ON
    BA_ON = bool(P.get("birth_age")) and BAT   # late births: own births by real fertility for age and sex
    RP_ON = bool(P.get("role_practice"))        # what one holds is practice too
    HH_ON = bool(P.get("hh_money"))   # F3 D1, D2: a child's money is the household's until they live on their own
    TP_ON = bool(P.get("ties_people"))   # F3 D3: ties are the people around them
    if HH_ON or TP_ON:
        if WON:
            B_PAR_ = WLM.PM.BIT["parent"]
        HH_CLS_ = np.asarray(P["hh_cls"], float); HH_E_ = P["hh_earn"]; TW_ = np.asarray(P["tie_w"], float)
        MO_ = P["mort"]
        _H = lambda x_: MO_[0] / MO_[1] * (np.exp(MO_[1] * x_) - 1)   # (seed library: no one is counted, so kin by the life table)

        def home_share(age):
            """F3: the share of their money that is already their own (0 a child at home, 1 on their own), and whether they
            live on their own."""
            ramp_ = _uclip((age - P["hh_ages"][0]) / max(P["hh_ages"][1] - P["hh_ages"][0], 1e-9), 0, 1)
            if WON:
                away_ = np.asarray(WL.PP.own_home, bool).copy()
            else:   # world off: a partner or a child of their own, no parent left, or 30
                away_ = held[:, PAR] | held[:, KID] | (age >= 30) | ((alive[:, 0] <= 0) if BAT else False)
            return np.where(away_, 1.0, ramp_ * (1 - P["hh_work"] + P["hh_work"] * held[:, CAR])), away_

        def household(age):
            """F3 D1, D2: the household's money level (class x the parents' work) and the family's floor level (class x
            closeness to a living parent)."""
            if WON:
                PP_ = WL.PP
                par_ = PP_.used & PP_.lv & ((PP_.rmask & B_PAR_) != 0)
                hj_ = np.asarray(PP_.hhj)
                in_ = (((PP_.mset >> np.maximum(hj_, 0).astype(PP_.mset.dtype)[:, None]) & 1) > 0) & (hj_ >= 0)[:, None]
                ern_ = (par_ & PP_.emp & in_).sum(1) + 0.5 * (par_ & PP_.emp & ~in_).sum(1)
                lv_ = HH_CLS_[_uclip(np.asarray(PP_.cls), 0, 2)]
                pc_ = np.where(par_, PP_.c, 0.0).max(1)
            else:
                np_ = alive[:, 0] if BAT else 2 * np.exp(-(_H(age + 30) - _H(30.0)))
                ern_ = np.minimum(np_, 2); lv_ = hh_res0 / max(HH_E_[0] + 2 * HH_E_[1], 1e-9)
                pc_ = 0.8 * (np_ > 0.5)
            return lv_ * (HH_E_[0] + HH_E_[1] * np.minimum(ern_, 2)), lv_ * pc_

        def ties_off(age, away_):
            """F3 D3, world off: ties from who is alive and held (parents, siblings, the closest friend, grandparents, the
            partner, children, community, work, faith)."""
            if BAT:
                kin_ = np.stack([np.minimum(alive[:, 0], 2), np.minimum(alive[:, 1], 3), np.minimum(alive[:, 2], 1),
                                 np.minimum(alive[:, 3], 3), held[:, PAR], np.minimum(np.maximum(alive[:, 5], held[:, KID]), 3)], 1)
            else:
                pa_ = 2 * np.exp(-(_H(age + 30) - _H(30.0))); ga_ = 3 * np.exp(-(_H(age + 58) - _H(58.0)))
                kin_ = np.stack([np.full(N, pa_), np.full(N, 1.3), np.full(N, 1.0), np.full(N, ga_), held[:, PAR],
                                 held[:, KID] * 2.0], 1)
            kin_[:, 0] = kin_[:, 0] * np.where(away_, P["tie_away"], 1.0)
            s_ = kin_ @ TW_[:6] + held[:, [COM, CAR, FAI]] @ TW_[6:9]
            return 1 - np.exp(-s_ / P["tie_T"])
    OR_ON = bool(P.get("one_roll"))   # F7: one roll of the living (the children at home by the youngest)
    BORN_S_ = L["names"].index("a child is born") if OR_ON and BAT and "a child is born" in L["names"] else -1
    RE_ON = bool(P.get("retire_ends")) and BAT   # F8: retirement ends work
    if RE_ON:
        import world_keys as WKR_
        WAT_ = np.asarray(L.get("W_AT", np.full(L["S"], -1)))
        lf1_ = np.array([(s_.get("life") or "").split(",")[0].strip() == "work" for s_ in L.get("src", [{}] * L["S"])])
        door_ = (L["COMMIT"] == CAR).any(1)                   # a door back: an option that starts a career
        WORK_S = ((lf1_ | (WAT_ == WKR_.INST_KINDS.index("employer"))) & ~door_)   # the forced S3/S4/S7 moments too (F8 thread, 10-12)
    WO_ON = bool(P.get("world_only")) and BAT   # F10: a world moment only on the world's event
    if WO_ON:
        WMZ_ = np.zeros(L["S"], bool)
        if WON:
            WMZ_[np.asarray(WL.wm_s, int)] = True
            REG_ = REG_ & ~WMZ_; ROUT_ = ROUT_ & ~WMZ_
        tl_ = np.array([s_.get("tier") == "life event" for s_ in L.get("src", [{}] * L["S"])])
        WG_ = (PERY.sum(1) == 0) & tl_ & GAPM_ & ~WMZ_          # waits for the world, with a gap: (the T4 seasons)
        WG_I = np.nonzero(WG_)[0]; WGLO_ = np.nan_to_num(GAP_[WG_I, 0])[None]
        WGW_ = np.maximum(np.nan_to_num(GAP_[WG_I, 1] - GAP_[WG_I, 0]), 1 / 52)[None]
    AF_ON = bool(P["age_free"]) and BAT                   # F9: life events by age, not by the life stage reached
    if AF_ON:
        AF_S = np.array([nm_ in set(P["age_free"]) for nm_ in np.asarray(L["names"], dtype=object)[np.asarray(L.get("ROOT", np.arange(L["S"])))]])
        AF_P = PERY[AF_S].max(1)[None]
    BW_ON = P["birth_with"] is not None and BA_ON         # F9.2: own births by the partnership
    if BW_ON:
        BW_ = np.asarray(P["birth_with"], float)
        BW_I = [i_ for i_, x_ in enumerate(GR["names"]) if x_ in HOME_TOGETHER] if RON else []
        hm_t = np.full(N, 10 ** 9)                        # the week the present home together began
    NE_ON = P["nest"] is not None and BAT                 # F9.5: the children leave home when the youngest is grown
    if NE_ON:
        NE_S = np.asarray(L["names"], dtype=object)[ROOT] == "the children leave home"
        NE_A, NE_R = P["nest"]
    AR_ON = bool(P["age_rate"]) and BAT                   # F9.24: life events at a rate by age, not stepping with the stage
    if AR_ON:
        AR_S = np.array([nm_ in set(P["age_rate"]) for nm_ in np.asarray(L["names"], dtype=object)[np.asarray(L.get("ROOT", np.arange(L["S"])))]])
        AR_X = STAGE_HI.copy(); AR_R = PERY[AR_S]
        AR_P = [(AR_X, r_) for r_ in AR_R]
        if P["age_pts"]:   # F9.23: an event's own rate points by age (a child version counts as one)
            AR_NM = np.asarray(L["names"], dtype=object)[np.asarray(L.get("ROOT", np.arange(L["S"])))][AR_S]
            AR_P = [tuple(np.asarray(P["age_pts"][nm_], float).T) if nm_ in P["age_pts"] else p_ for nm_, p_ in zip(AR_NM, AR_P)]
    if BA_ON:
        BIRTH_S = np.array([nm_ in BIRTH_OWN for nm_ in L["names"]])
        # the rate keeps its mean over the moment's own age window, so the births come when they do in real life
        ag_w = [np.arange(int(L["AGE"][s_, 0]), int(L["AGE"][s_, 1]) + 1) for s_ in np.nonzero(BIRTH_S)[0]]
        BA_NF = np.array([max(fert(a_, FERT_F).mean(), 1e-6) for a_ in ag_w])
        BA_NM = np.array([max(fert(a_, FERT_M).mean(), 1e-6) for a_ in ag_w])
        BF_ON = bool(P["birth_free"])
        BF_P = PERY[BIRTH_S].max(1)[None]   # birth_free: each own-birth moment at its highest stage rate
        # a choice that starts a child of one's own (not adopting, fostering or taking a child in)
        BIRTH_O = np.zeros(L["COMMIT"].shape, bool)
        for s_ in range(L["S"]):
            if L["TIER"][s_] != 1:
                for a_ in range(len(L["labels"][s_])):
                    BIRTH_O[s_, a_] = L["COMMIT"][s_, a_] == KID and not BIRTH_NOT.search(L["labels"][s_][a_])
        ba_rng = np.random.default_rng([int(seed), 83])
