# run_11_choice.py: part 11 of 18 of engine._run, the life loop.
# 2. the choice ("choose" pause) and 3. the outcome ("odds" and "learn" pauses), memory.
# Lines here are _run's own, unchanged and at their own indent: engine.py joins the parts in order (engine.RUN_PARTS)
# and compiles them as one, so a name used here may be set in an earlier part. Never import or run it alone.
        # ---- 2. choice
        if DOM_ON:   # in an area of life the colors that weigh the options are the core plus that area's offset
            area_ = L["AREA"][s]; inA_ = area_ >= 0
            zA_ = z + np.where(inA_[:, None], Dz[ar, np.maximum(area_, 0)], 0.0)
            w_hat = softmax(zA_ + P["act"] * alpha)
        else:
            w_hat = softmax(z + P["act"] * alpha)
        a_hat = softmax(y + P["act"] * alpha)
        V = np.einsum("nc,nkc->nk", w_hat, e)            # what current motives value
        VA = np.einsum("nc,nkc->nk", a_hat, e)           # what the person wants to value
        # reading the moment (Emren 09:25, point 8): with experience a person senses part of what the moment calls for and
        # how the world around them pushes, so felt odds spread like the true ones (the rest stays a misread)
        read_ = P["read_moment"][0] + P["read_moment"][1] * M / (M + P["M0"])
        mom_ = np.einsum("nkc,nc->nk", m, f_tot) + P["fit"] * np.einsum("nkc,nc->nk", m, alpha - alpha.mean(1, keepdims=True))
        readk_ = read_[:, None]   # per option; read_skill: expertise reads the moment, skill in its ways fills part of the rest
        if P["read_skill"]:
            readk_ = readk_ + P["read_skill"] * _uclip(np.einsum("nkc,nc->nk", m, sig - 0.3) / 0.7, 0, 1) * (1 - readk_)
        # v10 interpretation: threat focus follows where the deep core sits on security vs freedom, hard times and reactivity
        thr += (1 / (1 + np.exp(-(P["thr0"] + P["thr_axis"] * 5 * (softmax(k) @ AXSEC) + P["thr_hist"] * (wound + 0.5 * trouble)
                                  + P["thr_react"] * (react - 1)))) - thr) / (52 * P["thr_lag"])
        if MIS_ON:   # how the person misreads the odds (felt odds only): focus, memories, scars, mood, status; expertise shrinks it
            mis_ = (P["mis_focus"] * (0.5 - thr) + P["mis_mood"] * mood + P["mis_status"] * hub_)[:, None] \
                + np.einsum("nkc,nc->nk", m, P["mis_mem"] * mem_rel() - P["mis_scar"] * scar)
            if P["mis_expert"]:
                mis_ = mis_ / (1 + P["mis_expert"] * np.minimum(np.einsum("nkc,nc->nk", m, xp_), 3))
        else:
            mis_ = 0.0
        p_hat = 1 / (1 + np.exp(-earned(P["gain"] * (np.einsum("nkc,nc->nk", m, sig + fb) + readk_ * mom_ - diff)
                                        + TON * P["o_bias"] * (outlook - P["o_ref"])[:, None] + pbump + mis_, earn)))   # outlook: optimism or pessimism
        p_hat = np.where(do_nothing, 0.5, p_hat * lackf)   # lacking: the felt odds see it too
        if SEEN_ON:   # S6: a path or colour way seen walked feels more possible, one seen failing less (felt odds only)
            p_hat = WL.seen_felt(p_hat, s, m, ~do_nothing, mask)
            if BT_ON:   # body_trust: a pursuit in a sphere's bodies feels likelier with trust in them (felt odds only)
                p_hat = WL.trust_felt(p_hat, s, ~do_nothing)
        H = np.einsum("nkc,nc->nk", m, habit)             # habit is a pull toward familiar ways of acting
        lack = nimp * np.maximum(0, P["need_set"] - need) / P["need_set"] + P["duty_w"] * np.minimum(1, (held * I) @ DUTY)   # N,J
        serves = np.einsum("njc,nkc->nkj", NMP, np.maximum(e, 0)) if NM_ON else \
            np.einsum("jc,nkc->nkj", NMAP, np.maximum(e, 0))            # needs each option meets
        relief = np.einsum("nj,nkj->nk", lack, serves) * p_hat
        # gate 1, the world: is the option open to this person at all?
        acc = _uclip(P["access_base"] + P["access_k"] * (np.einsum("nkc,nc->nk", m, nic) - 0.2), 0.05, 1.0)
        if BAT and CLU_ON:
            acc = acc * P["closed_acc"] ** clu_
        elif BAT:
            acc = np.where(closed_s >= 0, acc * P["closed_acc"], acc)
        if OWN_ON:   # v22.5, F12: the culture's own acts are always around them (the means gate below still holds)
            acc = np.where(L["OWN"][s], 1.0, acc)
        req = L["REQ"][s]                                    # what each option needs: money, time, health, ties, freedom
        rg = np.where(req > 0, 1 / (1 + np.exp(-P["req_g"] * (res[:, None, :] - req))), 1.0).prod(-1)
        open_n = rng.random(mask.shape) < acc; open_r = rng.random(mask.shape) < rg
        open_ = mask & ((open_n & open_r) | do_nothing)
        # gate 2, the mindset: is an open option even considered? (fit with the deep core)
        kw = softmax(k)
        # v6 (Fredrickson 2001): a good mood widens what a person considers, a bad one narrows it to their usual ways
        ng = P["notice_g"] * (1 - P["broaden"] * _uclip(2 * (content - 0.5) + mood, -1, 1))
        see = 1 / (1 + np.exp(-(P["notice_b"] + ng[:, None] * (5 * np.einsum("nkc,nc->nk", m, kw) - 1) + gN)))   # v7: goals draw the eye
        seen = open_ & ((rng.random(mask.shape) < see) | do_nothing)
        # gate 3, wanting versus pull: reflective (aspiration, odds) vs automatic (motives, habit)
        step = 5 * np.einsum("nkc,nc->nk", m, softmax(y) - w)   # acting the way you want to become
        tryf = 1 + TON * P["o_try"] * (outlook - P["o_ref"])            # a sense of control makes people try to change
        U_R = (P["beta_V"] * VA + P["beta_A"] * tryf[:, None] * step + P["beta_P"] * (p_hat - 0.5) * stakes[:, None]
               + P["beta_N"] * relief)
        U_I = P["beta_V"] * V + P["beta_H"] * (1 + stress[:, None]) * H + P["beta_N"] * relief
        # roles: each held commitment expects its own ways of acting, felt as duty and as routine
        DW = (L["DOM"][s] + P["role_base"]) * held * I
        role = np.einsum("nk,nko->no", DW, 5 * np.einsum("nkc,noc->nko", prof, m) - 1)
        U_R = U_R + P["beta_role"] * role; U_I = U_I + P["beta_role"] * role
        U_R = U_R + gU_R; U_I = U_I + gU_I                   # v7: dreams, passions and plans
        if P["scar_pull"]:                                   # v10: never again, in the ways of a scar
            scU = P["scar_pull"] * np.einsum("nkc,nc->nk", m, scar); U_R = U_R - scU; U_I = U_I - scU
        if P["hz_k"]:                                        # v7: with time felt short, closeness, care and the familiar weigh more
            hzU = P["hz_k"] * fhz[:, None] * np.einsum("nkc,c->nk", 0.5 * (m + e), HZT)   # in its ways and for its ends
            U_R = U_R + hzU; U_I = U_I + hzU
        if len(ri):                                          # walking away costs what was invested; wanting out helps
            built = 5 * (prof[ri, rkk] * softmax(k[ri])).sum(1)      # how much of the deep self was built on it (1 = neutral)
            xc = P["beta_exit"] * EXITW[rkk] * I[ri, rkk] * (0.5 + 0.5 * built)   # sunk cost: leaving betrays that self
            U_R[ri, 2] += -xc + P["beta_A"] * 3 * misfit[ri, rkk]
            U_I[ri, 2] += -xc
        if WON:   # the world: felt reach makes voice and organising at institutions and the state feel worth it (spec 7 §6)
            rU_ = WL.reach_pull(s); U_R = U_R + rU_; U_I = U_I + rU_
            if P.get("sph_fair"):   # spheres phase 4: felt fairness tilts exit, neglect and subvert against voice and loyalty
                fU_ = WL.fair_pull(s) * (P["tau0"] * (1 + 0.5 * stress))[:, None]   # log odds x the choice's tau
                U_R = U_R + fU_; U_I = U_I + fU_
            if BT_ON:   # body_trust: low trust in a sphere's bodies tilts exit and neglect (and subvert) against voice, high
                bU_ = WL.trust_pull(s) * (P["tau0"] * (1 + 0.5 * stress))[:, None]   # trust voice and loyalty (log odds x tau)
                U_R = U_R + bU_; U_I = U_I + bU_
            if ODD_ON_:   # S4: an unplayed life holds on more where its colour is strong and its rung high (log odds x tau)
                oU_ = WL.eyes_pull(s) * (P["tau0"] * (1 + 0.5 * stress))[:, None]
                U_R = U_R + oU_; U_I = U_I + oU_
        if SHON:   # overuse ("when all you have is a hammer"): the shadow pulls toward its colour's ways, fitting or not
            shU_ = P["sh_over"] * np.einsum("nkc,nc->nk", m, shA); U_R = U_R + shU_; U_I = U_I + shU_
        ctrl = np.minimum(1, CTRL[stage] * dsc * _uclip(1 - P["ctrl_stress"] * stress, 0.05, 1)
                          * _uclip(1 + P["peace_ctrl"] * (peace - 0.55), 0.5, 1.3))     # a calm mind steers better
        U = ctrl[:, None] * U_R + (1 - ctrl[:, None]) * U_I
        if DC_ON:   # F17: an option that leaves a deed leans by that deed's canon colours (log odds x the choice's tau)
            U = U + P["deed_canon"] * np.einsum("nkc,nc->nk", DC_L[s], 5 * w - 1) * (P["tau0"] * (1 + 0.5 * stress))[:, None]
        if PT_ON and pt_pull.any():   # part 4: the pull back: options that break the law x 1.2 (log odds x the choice's tau)
            U = pt_pull_u(U, pt_pull, PT_BL[s], P["tau0"] * (1 + 0.5 * stress), PT_PULL)
        U = np.where(do_nothing, -0.3 + 0.3 * stress[:, None], U)
        tau = P["tau0"] * (1 + 0.5 * stress)
        pr = pr0 = softmax(np.where(seen, U / tau[:, None], -np.inf))
        if P["steer"] is not None:   # the player's steer (P3): it bends the character's own pick, then it is spent
            mix_ = np.asarray(P["steer"], float); mix_ = mix_ / np.maximum(mix_.sum(-1, keepdims=True), 1e-9)
            sU_ = np.where(do_nothing, 0.0, P["steer_k"] * (5 * np.einsum("nkc,nc->nk", m, np.broadcast_to(np.atleast_2d(mix_), (N, C))) - 1))
            pr = softmax(np.where(seen, (U + sU_) / tau[:, None], -np.inf))
            P["steer"] = None
        if SAC_ON_ and WL.sac_pend:   # S5: at an offer on a held line the character's own pick holds it at .9 (and more
            pr = WL.sacred_tilt(s, pr.copy(), mask)   # for a bigger offer, .7 with a gesture); at a tragic one, a, b or torn
        bou_ = rng.random((N, 1))
        a = (pr.cumsum(1) > bou_).argmax(1)
        if BO_ON:   # bold ways, in a week the game asks: each bold way open to them is a slot beside its base way, and the
            bold_pick[:] = -1; bo_row[:] = -1; bo_base[:] = -1; bo_seed[:] = -1; bold_now = None   # character's own pick
            if P["bold_ask"]:   # re-picks with the same draw over the ways and the slots seen
                bold_now = [[] for _ in range(N)]
                for n in np.nonzero(~dead & ~recon)[0]:
                    bow_ = np.zeros(2)
                    for boj_, bori_ in enumerate(BO_S.get(int(s[n]), ())):
                        bor_ = BO_ROWS[bori_]; bok_ = bor_["base"]
                        if not mask[n, bok_] or bor_["req"] and not (RON and r_has[n, bor_["req"]].any()) \
                                or P["title_ages"] and not bor_["ages"][0] <= t / 52 <= bor_["ages"][1]:
                            continue   # its base way open, its own requires: held, and what it gives inside its ages
                        boma_ = m[n, bok_]   # the base way's true odds, as the odds draw below has them
                        boz_ = P["gain"] * ((boma_ * (sig[n] + f_tot[n])).sum() + P["fit"] * (boma_ * (alpha[n] - alpha[n].mean())).sum()
                                          - diff[n, bok_]) + (pbump[n, bok_] if RON else 0.0) - (P["sh_fail"] * (boma_ * shA[n]).sum() if SHON else 0.0)
                        bopt_ = 1 / (1 + np.exp(-earned(boz_, earn[n, bok_] if np.ndim(earn) else 0.0))) * (lackf[n, bok_] if np.ndim(lackf) else 1.0)
                        boph0_ = min(max(float(p_hat[n, bok_]), 1e-6), 1 - 1e-6); bophb_ = bo_odds(n, bor_, boph0_)   # and as felt
                        bo_row[n, boj_] = bori_; bo_base[n, boj_] = bok_; bo_ph[n, boj_] = bophb_
                        bold_now[n].append(dict(row=int(bori_), slot=boj_, base=int(bok_), label=bor_["label"], chance=bor_["chance"],
                                                p=round(bo_odds(n, bor_, bopt_), 4), seen=bool(seen[n, bok_])))
                        if seen[n, bok_]:   # its utility is the base way's, with the felt odds' stake and relief moved
                            bodu_ = ctrl[n] * P["beta_P"] * (bophb_ - boph0_) * stakes[n] + P["beta_N"] * relief[n, bok_] * (bophb_ / boph0_ - 1)
                            bow_[boj_] = pr[n, bok_] * np.exp(min(bodu_ / tau[n], 50.0))
                    if bow_.sum() > 0:
                        box_ = np.concatenate([pr[n], bow_]); boi_ = int((box_.cumsum() / box_.sum() > bou_[n, 0]).argmax())
                        bokk_ = pr.shape[1]
                        a[n] = bo_base[n, boi_ - bokk_] if boi_ >= bokk_ else boi_
                        bold_pick[n] = boi_ - bokk_ if boi_ >= bokk_ else -1
                if P["bold_ask"] != "all":
                    P["bold_ask"] = False
        if SHON:   # U indecisive: while they weigh it, the chance passes (the act becomes doing nothing, where there is one)
            lap_ = (rng.random(N) < P["sh_lapse"] * shA[:, 1]) & ~do_nothing[ar, a] & do_nothing.any(1)
            if lap_.any():
                a = np.where(lap_, do_nothing.argmax(1), a)
        if pausing:
            steer_moved = pr[ar, a] - pr0[ar, a]   # how much the steer raised (or lowered) the drawn option's odds
            a_self = a.copy()                      # the character's own pick (a counter-pick lowers its shadow)
            _pause_state(pz_st, ST_CELLS, ST_FR)
            a = yield Pause("choose", t, pz_st, a)
            pz_st._fr = None
        if BO_ON:   # the slot taken: the game's (bold_take: a slot, with a its base way; -1 an ordinary way), else the
            bot_ = P["bold_take"]; P["bold_take"] = None   # character's own while its base way stands
            if bot_ is not None:
                bot_ = np.broadcast_to(np.asarray(bot_, int), (N,)); bosl_ = np.clip(bot_, 0, 1)
                bold_pick[:] = np.where((bot_ >= 0) & (bot_ <= 1) & (bo_row[ar, bosl_] >= 0) & (a == bo_base[ar, bosl_]), bot_, -1)
            else:
                bold_pick[:] = np.where((bold_pick >= 0) & (a == bo_base[ar, np.maximum(bold_pick, 0)]), bold_pick, -1)
        # bookkeeping: where does the option the person most wants get lost?
        UR_ = np.where(mask & ~do_nothing, U_R, -np.inf)
        best = UR_.argmax(1); has = np.isfinite(UR_.max(1))
        lost_open = has & ~open_[ar, best]; lost_seen = has & open_[ar, best] & ~seen[ar, best]
        pulled = has & seen[ar, best] & (a != best); tried = has & (a == best)
        pull_best = np.where(seen & ~do_nothing, U_I, -np.inf).argmax(1)
        conflict = has & seen[ar, best] & (pull_best != best)
        big_gap = 0.5 * np.abs(softmax(y) - w).sum(1) > 0.1; hi_s = stress > 1
        ma = m[ar, a]; ea = e[ar, a]; ea0 = e0[ar, a]; da = diff[ar, a]; ph = p_hat[ar, a]
        if BO_ON and (bold_pick >= 0).any():   # a bold pick: its felt odds are the bold way's
            ph = np.where(bold_pick >= 0, bo_ph[ar, np.maximum(bold_pick, 0)], ph)
        idle = do_nothing[ar, a] | dead                 # a life that has ended does nothing
        if BAT and IDC_ON:   # N1b: how far this week's act crossed the role expected of them (role_fit, the game's frown)
            act_cw = cw_[ar, a] * ~idle
        blocked += has & lost_open

        # ---- 3. outcome vs expectation
        fit = P["fit"] * (ma * (alpha - alpha.mean(1, keepdims=True))).sum(1)
        shc_ = P["sh_fail"] * (ma * shA).sum(1) if SHON else 0.0   # shadows: over-reliance on a ruling colour costs
        p_true = 1 / (1 + np.exp(-earned(P["gain"] * ((ma * (sig + f_tot)).sum(1) + fit - da) + (pbump[ar, a] if RON else 0.0) - shc_,
                                         earn[ar, a] if np.ndim(earn) else 0.0)))
        if np.ndim(lackf):
            p_true = p_true * lackf[ar, a]
        if BAT:   # for the Library's chance (batch.CHANCE_REF): skill, world and perks of those who meet each moment, and the
            # true odds of every option for them (calib_v7/chance_check.py)
            rf_ = sig + f_tot + (PB / P["gain"] if RON else 0.0)
            np.add.at(ref_sum, s, rf_); np.add.at(ref_cnt, s, 1.0)
            fk_ = P["fit"] * np.einsum("nkc,nc->nk", m, alpha - alpha.mean(1, keepdims=True))
            pk_ = 1 / (1 + np.exp(-earned(P["gain"] * (np.einsum("nkc,nc->nk", m, sig + f_tot) + fk_ - diff) + pbump
                                          - (P["sh_fail"] * np.einsum("nkc,nc->nk", m, shA) if SHON else 0.0), earn)))
            pk_ = pk_ * lackf                                  # as the engine draws them: earned odds and lacking: included
            if np.ndim(earn):   # the mean earned lift on the options that give a title, for the reference (CHANCE_REF's 6th)
                tk_ = GR["A_EARN"][s] >= 0
                np.add.at(earn_sum, s, (earn * tk_).sum(1) / np.maximum(tk_.sum(1), 1)); np.add.at(earn_cnt, s, tk_.any(1).astype(float))
            np.add.at(pk_sum, s, np.where(mask, pk_, 0.0)); np.add.at(pk_cnt, s, mask.astype(float))   # open to them
        if BO_ON and (bold_pick >= 0).any():   # a bold pick: its base way drawn at the bold way's own odds
            for n in np.nonzero(bold_pick >= 0)[0]:
                p_true[n] = bo_odds(n, BO_ROWS[bo_row[n, bold_pick[n]]], p_true[n])
        if pausing:
            _pause_state(pz_st, ST_CELLS, ST_FR)
            p_true = yield Pause("odds", t, pz_st, p_true)
            pz_st._fr = None
        succ = rng.random(N) < p_true
        if BO_ON and (bold_pick >= 0).any():
            for n in np.nonzero(bold_pick >= 0)[0]:
                bor_ = BO_ROWS[bo_row[n, bold_pick[n]]]
                bold_log.append((int(n), t, int(bor_["i"]), int(bold_pick[n]), round(float(p_true[n]), 4), bool(succ[n])))
                if n in events:
                    events[n].append(dict(bold=dict(age=round(age, 2), row=int(bor_["i"]), slot=int(bold_pick[n]), label=bor_["label"],
                                                    moment=bor_["moment"], colour=COLORS[bor_["colour"]],
                                                    p=round(float(p_true[n]), 4), ok=bool(succ[n]))))
        if BT_ON:   # body_trust: an own run-in with a body this week, gone well (good) or against them (bad)
            ri_ = ~idle & ~recon & ~dead & (BT_RUN[s] >= 0)
            for j_ in np.unique(BT_RUN[s][ri_]).tolist():
                WL.PP.bt_jump(np.nonzero(ri_ & succ & (BT_RUN[s] == j_))[0], j_, BTJ_["own_run_in_good"], "good")
                WL.PP.bt_jump(np.nonzero(ri_ & ~succ & (BT_RUN[s] == j_))[0], j_, BTJ_["own_run_in_bad"], "bad")
        if SHON:   # a shadow shows: an act in the ruling colour's own ways fails while its shadow is strong (check 5)
            shw_ = (ma * shA)
            for n in np.nonzero(~succ & ~idle & (shw_.max(1) > 0.3))[0]:
                c_ = int(shw_[n].argmax()); sh_n[n, c_] += 1
                sh_log.append((int(n), t, c_, int(s[n]), int(a[n])))
                if n in events:
                    events[n].append(dict(shadow=dict(age=round(age, 2), state=SH_STATES[c_], strength=round(float(shA[n, c_]), 2),
                                                      through=L["labels"][s[n]][a[n]])))
        long_miss = (~succ & ~idle & ~recon & (p_true < P["long_shot"]) & (LONGT_[s, a] | (missed_at(GR["A_TITLE"][s, a], s, a) >= 0))
                     ) if RON else np.zeros(N, bool)
        if RON:   # a failed try at a title (else a perk with its own helps) is remembered for the next (try_lift)
            ae_ = missed_at(GR["A_EARN"][s, a], s, a)
            ft_ = np.nonzero(~succ & ~idle & ~recon & (ae_ >= 0))[0]
            if len(ft_):
                ti_ = ae_[ft_]; tries_ct[ft_, ti_] = np.minimum(tries_ct[ft_, ti_] + 1, 100)
        tries += tried; wins += tried & succ
        np.add.at(gates, stage, np.stack([has, lost_open, lost_seen, pulled, tried, tried & succ, conflict, conflict & (a == best),
                                     conflict & big_gap, conflict & big_gap & (a == best), conflict & hi_s, conflict & hi_s & (a == best),
                                     has & ~open_r[ar, best], has & open_r[ar, best] & ~open_n[ar, best]], 1).astype(float))
        r = np.where(succ, 1.0, -P["loss"]) * stakes
        delta = np.where(idle, 0.0, r - (ph - (1 - ph) * P["loss"]) * stakes)
        if pausing:
            _pause_state(pz_st, ST_CELLS, ST_FR)
            delta = yield Pause("learn", t, pz_st, delta)
            pz_st._fr = None
        appf_ = 1 + P["app_k"] * (2 * thr - 1)              # v10 appraisal: a loss weighs appf_, a gain 2 - appf_
        fdelta = delta * np.where(delta < 0, appf_, 2 - appf_) if P["app_k"] else delta   # as felt (mood, stress, wounds)
        if P["app_vigil"] and P["app_k"]:   # app_vigil: threat focus learns more from gains and losses alike (vigilance), so
            ldelta = delta * (1 + P["app_learn"] * (appf_ - 1))   # the colours that bring it (W U, AXSEC) do not teach a life out of themselves
        else:
            ldelta = delta + P["app_learn"] * (fdelta - delta) if P["app_learn"] else delta   # as learned (which ways to keep)
        act_ = (~idle)[:, None]
        fb += 0.05 * ((succ.astype(float) - ph)[:, None] * ma) * act_
        sig += P["skill_gain"] * ma * (1 - sig) * act_            # skill grows with practice in a color's ways
        if CU_ON:   # C2: understanding keeps into later life (Blue skill fades more slowly from cu_age); C3 reads its growth
            sg0_ = sig[:, 1].copy()
            sig -= P["skill_fade"] * (sig - 0.3) * (1 - ma) * np.where((np.arange(C) == 1)[None] & (age >= P["cu_age"]),
                                                                       1 - P["cu_keep"], 1.0)
        else:
            sig -= P["skill_fade"] * (sig - 0.3) * (1 - ma)           # and fades back toward a beginner's level without it
        if RP_ON:   # role_practice: the ways of what one holds, at most one act's worth a week
            rw_ = np.einsum("nk,nkc->nc", held * I, prof); rs_ = rw_.sum(1, keepdims=True)
            rw_ = rw_ / np.maximum(rs_, 1.0) * ~dead[:, None]
            sig += P["role_skill"] * P["skill_gain"] * rw_ * (1 - sig) * (black_k()[:, None] if P["black_edge"] else 1.0)
        SE += 0.05 * ma * (succ[:, None] - SE) * act_
        habit = 0.99 * habit + 0.01 * ma * act_
        # v10 memory: how acts in each color's ways went, weighted by stakes; bad memories fade faster than good ones
        mem_s = mem_s * DMS_ + (stakes * succ)[:, None] * ma * act_
        mem_f = mem_f * DMF_ + (stakes * ~succ)[:, None] * ma * act_
        if P["scar_k"]:   # a failure at high stakes can leave a never-again scar in its ways; support heals it faster
            sc_ = ~succ & ~idle & (stakes >= P["scar_min"])
            scar += P["scar_k"] * (stakes * sc_)[:, None] * ma * (1 - scar)
            scar *= 0.5 ** ((1 + support)[:, None] / (52 * P["scar_half"]))

        held_wk = held.copy()
