# run_07_body.py: part 7 of 18 of engine._run, the life loop.
# The body, the mind and death (F1, F2): body_week(), death_week().
# Lines here are _run's own, unchanged and at their own indent: engine.py joins the parts in order (engine.RUN_PARTS)
# and compiles them as one, so a name used here may be set in an earlier part. Never import or run it alone.
    # ---- v22.5 F1 and F2: the body, the mind and death from the life, each behind its switch. Off, nothing here draws
    # or changes anything and health runs as before. The weekly steps are body_week() (in 3b, where health drifted) and
    # death_week() (in 4e, where the life table was read)
    BODY_ON = bool(P["body"]); MIND_ON = bool(P["mind"]); DTH_ON = bool(P["death_life"]); HM_ON = BODY_ON or MIND_ON
    BP_ = {**BODY_PAR, **(P["body_par"] or {})}; MP_ = {**MIND_PAR, **(P["mind_par"] or {})}
    DP2_ = {**DEATH_PAR, **(P["death_par"] or {})}
    BAGE_X, BAGE_Y = (np.asarray(x_, float) for x_ in zip(*BP_["age"]))   # the body's level by age, alone
    body_v = res[:, HEA].copy(); mind_v = np.full(N, float(MP_["start"]))  # the two halves of health
    hea_w = res[:, HEA].copy()                               # health as body_week last wrote it (what changed it since is a shock)
    bd_base = body_v.copy()                                  # the body's slow level, moving over years
    bd_ill = np.zeros(N); bd_inj = np.zeros(N); bd_preg = np.zeros(N)   # dips that heal in weeks: illness, injury, a birth
    bd_cw = np.zeros((N, 3)); bd_ck = np.full((N, 3), -1); bd_ca = np.zeros((N, 3))   # up to three long-term conditions:
                                                             # weight, kind (COND_KINDS), age at onset
    bd_ser = np.zeros(N); bd_sk = np.full(N, -1); bd_s0 = np.full(N, NEVER); bd_s1 = np.full(N, NEVER)   # a serious illness:
                                                             # its dip, kind (SER_KINDS), first and last week
    bd_keep = np.zeros(N)                                    # what illness and injury took from the body for good
    bd_con = np.zeros(N); bd_strain = np.zeros(N); bd_money = res[:, MON].copy(); bd_carel = np.zeros(N)
    md_str = np.zeros(N); md_res = np.zeros(N)               # the mind: months of strain; resilience
    md_end = np.full((N, 3), NEVER)                          # the week each threat ends: a low season, anxiety, numbing
    dl_at = np.full(N, NEVER); dl_t0 = np.full(N, NEVER); dl_cause = [""] * N   # a last decline: its end and start, of what
    SER_CF = np.array([DP2_["ser_fatal"][k_] for k_ in SER_KINDS])   # each serious illness's share of courses that end in death
    CLETH_ = np.asarray(COND_LETHAL, float)
    HAB_ = np.add(np.add(BP_["rest"], BP_["move"]), BP_["moderate"]); BCARE_ = np.asarray(BP_["care"], float)
    BHEAL_ = np.asarray(BP_["heal"], float); BRISK_ = np.asarray(BP_["risk"], float)
    LK_B = ("condition", "serious", "accident or illness", "injury", "burnout"); LK_M = ("low", "anx", "numb")
    BL_K = np.array([LK_B.index(BODY_MOMENTS[L["names"][r_]]) if L["names"][r_] in BODY_MOMENTS else -1 for r_ in ROOT])
    ML_K = np.array([LK_M.index(MIND_MOMENTS[L["names"][r_]]) if L["names"][r_] in MIND_MOMENTS else -1 for r_ in ROOT])
    BL_ON = BODY_ON and bool(BP_["moments"]) and bool((BL_K >= 0).any())   # the Library's own body moments happen to the body
    ML_ON = MIND_ON and bool(MP_["moments"]) and bool((ML_K >= 0).any())
    BL_COND = BL_ON and bool((BL_K == 0).any()); BL_SER = BL_ON and bool(np.isin(BL_K, (1, 2)).any())   # else the engine's rates
    ML_HAS = [ML_ON and bool((ML_K == k_).any()) for k_ in range(3)]
    BL_S = np.nonzero(BL_K >= 0)[0]; ML_S = np.nonzero(ML_K >= 0)[0]
    if HM_ON:   # the outputs carry the two halves (V_hist body and mind) only with a switch on
        V_hist["body"] = []; V_hist["mind"] = []
    PREG_O = np.zeros(L["COMMIT"].shape, bool)               # a choice that begins a child of one's own (H7)
    for s_ in np.nonzero([nm_ in BIRTH_OWN for nm_ in L["names"]])[0] if BODY_ON else ():
        for a_ in range(len(L["labels"][s_])):
            PREG_O[s_, a_] = L["COMMIT"][s_, a_] == KID and not BIRTH_NOT.search(L["labels"][s_][a_])
    PG_ON = bool(PREG_O.any())
    if BODY_ON:   # H1 and an early condition: drawn from their own stream, so no other draw moves
        crng_ = np.random.default_rng([int(seed), 5101])
        bd_con = crng_.normal(0, BP_["con_sd"], N) - (crng_.random(N) < BP_["con_frail"][0]) * BP_["con_frail"][1]
        cy_ = crng_.random(N) < BP_["cond_young"]; cs_ = crng_.uniform(*BP_["cond_size"], N); ck_ = crng_.choice(len(COND_KINDS), N, p=COND_P[0])
        bd_cw[cy_, 0] = cs_[cy_]; bd_ck[cy_, 0] = ck_[cy_]; bd_ca[cy_, 0] = crng_.uniform(0, 6, N)[cy_]

    def body_log(n_, **rec):   # a logged life's body and mind record (the game tells what it wants of it)
        if n_ in events:
            events[n_].append(dict(body=dict(age=round(t / 52, 2), **rec)))

    def bd_condition(n_, kind=None):   # a long-term condition begins (H3), at most three
        j_ = int(np.argmin(bd_cw[n_]))
        if bd_cw[n_, j_] > 0:
            return
        k_ = kind if kind is not None else int(rng.choice(len(COND_KINDS), p=COND_P[0 if age < 16 else 1]))
        if P["cond_once"] and (bd_ck[n_] == k_).any():   # F9.27 (F10): one they have already is not diagnosed again
            return
        bd_cw[n_, j_] = rng.uniform(*BP_["cond_size"]) * (1 - 0.3 * float(np.clip(lean_c[n_], -1, 1))) * dip_f
        bd_ck[n_, j_] = k_; bd_ca[n_, j_] = age
        body_log(n_, kind="condition", name=COND_KINDS[k_], what="begins")

    def bd_serious(n_, kind):   # a serious illness begins (H6): a dip for months; early care finds it sooner
        if bd_sk[n_] >= 0 or dead[n_]:
            return
        bd_sk[n_] = kind; bd_s0[n_] = t
        bd_s1[n_] = t + int(4.33 * rng.uniform(*BP_["ser_months"]))
        bd_ser[n_] = rng.uniform(*BP_["ser_size"]) * (1 - 0.3 * float(np.clip(lean_c[n_], -1, 1))) * dip_f
        body_log(n_, kind="serious", name=SER_KINDS[kind], what="begins")

    def bd_injury(n_, lo, hi, told=True):   # an injury: a dip that heals in weeks, now and then with a lasting mark (H5);
        bd_inj[n_] += rng.uniform(lo, hi) * dip_f   # told=False when a Library moment already tells it
        if rng.random() < BP_["inj_keep"][0]:
            bd_keep[n_] += BP_["inj_keep"][1] * dip_f
        if told:
            body_log(n_, kind="injury", what="hurt")

    def md_threat(n_, k_, told=True):   # a low season, anxiety or numbing begins (or goes on), shorter with resilience
        mo_ = MP_[("low_months", "anx_months", "numb_months")[k_]]
        end_ = t + int(4.33 * rng.uniform(*mo_) * (1 - 0.5 * md_res[n_]))
        if end_ > md_end[n_, k_]:
            if md_end[n_, k_] <= t and told:
                body_log(n_, kind=("low season", "anxiety", "numbing")[k_], what="begins")
            md_end[n_, k_] = end_

    lean_c = np.zeros(N)   # this week's early-care lean (H11), read by the helpers above
    dip_f = 1.0            # this week's share an illness or injury takes (BODY_PAR dip_level), read by the helpers above

    def body_week(ht, ht0):
        """F1 in 3b, once a week from age 3: what changed health since last week reaches the body as a shock (a fall is an
        injury-like dip, a lift heals dips first), the body's and the mind's own events, each half moves, and health is
        written as their mean. ht is the old rule's level for the age with its work and title parts, ht0 its age part."""
        nonlocal lean_c, dip_f
        al_ = ~dead; ext_ = res[:, HEA] - hea_w
        dec_ = np.where(dl_at > NEVER // 2, _uclip((t - dl_t0) / np.maximum(dl_at - dl_t0, 1), 0, 1), 0.0) ** DP2_["decline_k"]   # F2: the decline
        lean_ = (w - 0.2) / 0.2                                  # each colour's share above or below even, per .2
        lean_c = lean_ @ BCARE_
        if BT_ON:   # body_trust: care seeking (1 + the early-care lean) x (.7 + .6 x btrust[care]), read back as the lean
            bc_ = btrust[:, BT_CARE_J]
            lean_c = bt_care(lean_c, bc_)
        tab_ = np.interp(age, BAGE_X, BAGE_Y)
        dip_f = float(tab_ / BAGE_Y.max()) if BP_["dip_level"] else 1.0
        low_ = md_end[:, 0] > t; anx_ = md_end[:, 1] > t; numb_ = md_end[:, 2] > t
        if BODY_ON:
            neg_ = np.maximum(-ext_, 0); pos_ = np.maximum(ext_, 0)
            bd_inj[:] += neg_
            h_ = np.minimum(pos_, bd_inj); bd_inj[:] -= h_; pos_ = pos_ - h_
            h_ = np.minimum(pos_, bd_ill); bd_ill[:] -= h_; bd_base[:] += pos_ - h_
            # the slow level: age, constitution, habits, strain, people, money, care, the mind, the work and titles (ht)
            bd_strain[:] += (stress - bd_strain) / (52 * BP_["strain_years"])
            bd_money[:] += (res[:, MON] - bd_money) / (52 * BP_["money_years"])
            mm_ = bd_money
            if WON:   # a child's money is the family's: its class
                mm_ = np.where(stage <= 1, np.array([0.08, 0.25, 0.5])[np.clip(np.asarray(WL.PP.cls), 0, 2)], bd_money)
            mods_ = (bd_con + lean_ @ HAB_ + BP_["disc"] * (dsc - 1) - 0.03 * numb_ - bd_keep + (ht - ht0)
                     - BP_["strain"] * _uclip((bd_strain - BP_["strain_from"]) / 1.0, 0, 1)
                     - BP_["lonely"] * _uclip((BP_["lonely_line"] - need[:, NIDX["belonging"]]) / 0.4, 0, 1)
                     + BP_["money"] * _uclip((mm_ - 0.2) / 0.2, -1, 1))
            if WON and getattr(WL.PP, "care_load", None) is not None:   # H16
                bd_carel[:] += (np.asarray(WL.PP.care_load, float) - bd_carel) / 104
                mods_ = mods_ - BP_["care_load"] * _uclip(bd_carel / 20, 0, 1)
            if MIND_ON:
                mods_ = mods_ - BP_["mind_wear"] * _uclip((0.6 - mind_v) / 0.4, 0, 1)
            tgt_ = toward(tab_, mods_)                            # around the age's level, never past 1
            bd_base[:] += (tgt_ - bd_base) * (1 - 0.5 ** (1 / (52 * BP_["base_half"])))
            # the dips heal: faster with early care and Green's and Red's ways, slower when poor or old
            slow_ = (1 + 0.3 * _uclip((0.15 - mm_) / 0.15, 0, 1)) * (1 + max(0.0, age - 60) / 40) \
                * (1 - 0.3 * _uclip(lean_c, -1, 1)) * (1 - 0.3 * _uclip(lean_ @ BHEAL_, -1, 1))
            bd_ill[:] *= 0.5 ** (1 / (BP_["ill_half"] * slow_)); bd_inj[:] *= 0.5 ** (1 / (BP_["inj_half"] * slow_))
            bd_preg[:] *= 0.5 ** (1 / BP_["preg_half"])
            # the body's own events this week: a short illness, an injury; a condition or a serious illness where the
            # Library has no moment for them; a young condition that eases; a serious illness that ends
            u_ = rng.random((N, 6))
            pi_ = np.interp(age, *zip(*BP_["ill_rate"])) * (1 + BP_["ill_mind"] * (low_ | anx_)) / 52
            ii_ = np.nonzero(al_ & (u_[:, 0] < pi_))[0]
            bd_ill[ii_] += (BP_["ill_size"][0] + (BP_["ill_size"][1] - BP_["ill_size"][0]) * u_[ii_, 5]) * dip_f
            pj_ = np.interp(age, *zip(*BP_["inj_rate"])) * np.exp(lean_ @ BRISK_) / 52
            for n_ in np.nonzero(al_ & (u_[:, 1] < pj_))[0]:
                bd_injury(n_, *BP_["inj_size"])
            rk_ = np.minimum(np.exp(BP_["risk_k"] * (tab_ - body_v)), 2.0)
            if not BL_COND:
                for n_ in np.nonzero(al_ & (u_[:, 2] < np.interp(age, *zip(*BP_["cond_rate"])) * rk_ / 52))[0]:
                    bd_condition(n_)
            if not BL_SER:
                for n_ in np.nonzero(al_ & (u_[:, 3] < np.interp(age, *zip(*BP_["ser_rate"])) * rk_ / 52))[0]:
                    bd_serious(n_, int(rng.choice(len(SER_KINDS), p=(0.45, 0.3, 0.15, 0.1))))
            if age < 18:   # H3: a young person's condition may ease
                for n_ in np.nonzero(al_ & (u_[:, 4] < BP_["cond_ease"] / 52) & (bd_cw[:, 0] > 0) & (bd_ca[:, 0] < 16))[0]:
                    body_log(n_, kind="condition", name=COND_KINDS[bd_ck[n_, 0]], what="eases")
                    bd_cw[n_, 0] = 0.0; bd_ck[n_, 0] = -1
            for n_ in np.nonzero((bd_sk >= 0) & (t >= bd_s1) & al_ & (dl_at <= NEVER // 2))[0]:   # through it: some stays
                bd_keep[n_] += rng.uniform(*BP_["ser_keep"]) * dip_f; body_log(n_, kind="serious", name=SER_KINDS[bd_sk[n_]], what="through it")
                bd_sk[n_] = -1; bd_ser[n_] = 0.0; bd_s0[n_] = bd_s1[n_] = NEVER
            if BL_ON or PG_ON:   # the Library's own body moments this week, and a birth of their own (H7)
                lk_ = np.where(~recon & al_, BL_K[s], -1)
                for n_ in np.nonzero(lk_ >= 0)[0]:
                    k_ = int(lk_[n_]); nm_ = L["names"][ROOT[s[n_]]]
                    if k_ == 0:
                        bd_condition(n_, COND_KINDS.index("arthritis") if "wild years" in nm_ else None)
                    elif k_ == 1:   # a diagnosis: most often cancer, else the heart or the lungs
                        bd_serious(n_, int(rng.choice(len(SER_KINDS), p=(0.6, 0.25, 0.0, 0.15))))
                    elif k_ == 2 and rng.random() < np.clip((age - 30) / 50, 0.05, 0.5):   # an illness more often with age
                        bd_serious(n_, 1 if rng.random() < 0.6 else 2)
                    elif k_ == 2:
                        bd_injury(n_, 0.3, 0.45, False)
                    elif k_ == 3:
                        bd_injury(n_, 0.12, 0.3, False)
                    else:   # burnout: the body runs down for weeks
                        bd_ill[n_] += 0.1
                pg_ = PREG_O[s, a] & succ & ~idle & female & ~recon & al_
                bd_preg[pg_] += BP_["preg"]
            body_v[:] = _uclip(bd_base - np.minimum(bd_cw.sum(1), BP_["cond_max"]) - bd_ser - bd_ill - bd_inj - bd_preg, 0.01, 0.99) \
                * (1 - 0.85 * dec_)
        else:   # health as before, as the body half
            body_v[:] = _uclip(body_v + ext_, 0, 1); body_v[:] += 0.01 * (ht - body_v)
        if MIND_ON:
            md_str[:] += (stress - md_str) / 13                    # the last three months' strain
            bel_ = need[:, NIDX["belonging"]]
            mods_ = (MP_["mood"] * (base_mood - MP_["mood_ref"]) + MP_["content"] * (content - MP_["content_ref"])
                     + np.where(stage == 0, 0.06, np.where(stage == 1, 0.03, 0.0))   # the family holds a child's mind up
                     - MP_["strain"] * _uclip(md_str - MP_["strain_from"], 0, 1) - MP_["loss"] * np.minimum(wound, 1.5)
                     - MP_["scar"] * np.minimum(scar.sum(1), 3.0) - MP_["lonely"] * _uclip((MP_["lonely_line"] - bel_) / 0.4, 0, 1)
                     + _uclip(MP_["meaning"] * (need[:, NIDX["meaning"]] - 0.9), -0.06, 0.06)
                     - MP_["rest"] * _uclip((0.15 - res[:, TIM]) / 0.1, 0, 1) - MP_["body"] * np.maximum(0.7 - body_v, 0)
                     - MP_["low_dip"] * low_ - MP_["anx_dip"] * anx_ - MP_["numb_dip"] * numb_ - 0.3 * dec_)
            tgt_ = toward(np.full(N, float(MP_["level"])), mods_)
            mind_v[:] += (tgt_ - mind_v) * (1 - 0.5 ** (1 / MP_["half"]))
            own_ = (5 * (ma * hold).sum(1) - 1 > 0) & succ & ~idle & ~recon   # steadier picks: an act that works and fits them
            mind_v[:] = _uclip(mind_v + MP_["steady"] * own_, 0.01, 0.99)
            # the threats: the Library's moments start a low season or numbing; anxiety (and the others, where a Library
            # has no moment for them) by the engine's rate, likelier as the mind falls, less likely with resilience
            if ML_ON:
                lk_ = np.where(~recon & al_, ML_K[s], -1)
                for n_ in np.nonzero(lk_ >= 0)[0]:
                    md_threat(n_, int(lk_[n_]), False)
            rk_ = np.minimum(np.exp(MP_["risk_k"] * (0.75 - mind_v)), 3.0) * (1 - md_res) * (age >= 8)
            u_ = rng.random((N, 3))
            for k_, rt_ in enumerate((MP_["low_rate"], MP_["anx_rate"], MP_["numb_rate"] * (age >= 14))):
                if not ML_HAS[k_]:
                    for n_ in np.nonzero(al_ & (u_[:, k_] < rt_ * rk_ / 52))[0]:
                        md_threat(n_, k_)
            # what a threat does while it lasts: a low season lowers the mood, anxiety strains, numbing eases the strain a
            # little now and wears self-control
            mood[low_] -= 0.01; stress[anx_] += 0.02; stress[numb_] = np.maximum(stress[numb_] - 0.01, 0); dsc[numb_] *= 0.998
            ov_ = (md_end > NEVER // 2) & (md_end <= t) & al_[:, None]   # a threat over: with people around, resilience grows
            for n_, k_ in zip(*np.nonzero(ov_)):
                if bel_[n_] >= 0.6:
                    md_res[n_] = min(MP_["resil_max"], md_res[n_] + MP_["resil"])
                body_log(n_, kind=("low season", "anxiety", "numbing")[k_], what="lifts")
                md_end[n_, k_] = NEVER
            hea_ = (1 - MP_["mind_w"]) * body_v + MP_["mind_w"] * mind_v
        else:
            hea_ = body_v
        res[:, HEA] = hea_; hea_w[:] = hea_

    def death_week():
        """F2 in 4e, once a week while self_death is on: a decline that has run its course ends the life; otherwise each
        cause's risk this week from the body and what they have, and a death drawn is sudden (an accident, a heart attack
        or a stroke) or comes after a last decline the story can tell."""
        for n_ in np.nonzero((dl_at > NEVER // 2) & (t >= dl_at) & ~dead)[0]:
            die(n_, dl_cause[n_])
        al_ = ~dead & (dl_at <= NEVER // 2)
        if BODY_ON:   # the body without a serious illness's own dip (its course has its own risk) or a birth's
            bod_ = _uclip(bd_base - np.minimum(bd_cw.sum(1), BP_["cond_max"]) - bd_ill - bd_inj, 0.01, 0.99)
        else:
            bod_ = body_v if HM_ON else res[:, HEA]
        gap_ = np.interp(age, BAGE_X, BAGE_Y) - bod_
        qa_ = np.interp(age, *zip(*DP2_["acc"])) * np.exp(DP2_["acc_red"] * (w[:, 3] - 0.2) / 0.2)
        fl_ = DP2_["frail_late"]
        gom_ = DP2_["frail"][1] * age + ((fl_[1] - DP2_["frail"][1]) * max(age - fl_[0], 0.0) if fl_ else 0.0)
        qf_ = (DP2_["frail"][0] * np.exp(gom_) + (DP2_["frail_c"] if age >= 15 else 0.0)) * np.exp(DP2_["frail_k"] * gap_)
        cl_ = bd_cw * np.where(bd_ck >= 0, CLETH_[np.maximum(bd_ck, 0)], 0.0)   # each condition's complications
        qc_ = DP2_["cond_k"] * cl_.sum(1) * np.exp(0.06 * (age - 50))
        cf_ = np.minimum(SER_CF[np.maximum(bd_sk, 0)] * float(np.clip(1 + DP2_["ser_age"] * (age - 60), *DP2_["ser_age_lim"]))
                         * np.exp(DP2_["frail_k"] * gap_ / 2), 0.95)
        wk_ = np.maximum(bd_s1 - bd_s0, 1)
        qs_ = np.where(bd_sk >= 0, 1 - (1 - cf_) ** (1 / wk_), 0.0)   # spread over the illness's weeks
        q_ = np.stack([qa_ / 52, qf_ / 52, qc_ / 52, qs_], 1)
        tot_ = 1 - np.prod(1 - np.minimum(q_, 1), 1)
        u_ = rng.random((N, 3))
        for n_ in np.nonzero(al_ & (u_[:, 0] < tot_))[0]:
            c_ = int(np.searchsorted(np.cumsum(q_[n_]) / q_[n_].sum(), u_[n_, 1]))
            if c_ == 0:
                die(n_, "in an accident"); continue
            if c_ == 1 and age < DP2_["old_age"] and u_[n_, 2] < DP2_["sudden"]:   # a failing body, at once
                die(n_, "of a sudden heart attack" if u_[n_, 2] < 0.7 * DP2_["sudden"] else "of a stroke"); continue
            if c_ == 3:
                why_, kd_ = {0: "of cancer", 1: "of heart disease", 2: "after a stroke", 3: "of lung disease"}[int(bd_sk[n_])], "serious"
            elif c_ == 1 and age >= DP2_["old_age"]:
                why_, kd_ = "old age", "old"
            elif c_ == 1 and not (cl_[n_] > 0).any():   # a failing body with nothing named: the heart, over weeks
                why_, kd_ = "of heart failure", "condition"
            else:   # a condition's complications (the one that weighs most): an asthma attack or a seizure is sudden
                k_ = int(bd_ck[n_, int(np.argmax(cl_[n_]))])
                if COND_KINDS[k_] in ("asthma", "epilepsy"):
                    die(n_, COND_DEATH[k_]); continue
                why_, kd_ = COND_DEATH[k_], "condition"
            dl_t0[n_] = t; dl_at[n_] = t + int(rng.uniform(*DP2_["decline"][kd_])); dl_cause[n_] = why_
            hz_mem[n_] += P["hz_remind"]
            if n_ in events:
                events[n_].append(dict(decline=dict(age=round(t / 52, 2), cause=why_, weeks=int(dl_at[n_] - t))))

