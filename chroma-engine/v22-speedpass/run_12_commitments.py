# run_12_commitments.py: part 12 of 18 of engine._run, the life loop.
# 3b. resources and commitments, money and debts, clashes; 3c. goals: steps, strength, plans.
# Lines here are _run's own, unchanged and at their own indent: engine.py joins the parts in order (engine.RUN_PARTS)
# and compiles them as one, so a name used here may be set in an earlier part. Never import or run it alone.
        # ---- 3b. resources and commitments (v4)
        res += act_ * (L["PAY"][s, a] + np.where(succ[:, None], L["WIN"][s, a], L["LOSE"][s, a]))
        ck = L["COMMIT"][s, a]
        if OR_ON and BORN_S_ >= 0:   # F7: the moment a child is born is the birth, however the act goes (a birth named once)
            bn_ = (s == BORN_S_) & ~recon & ~dead
            ck = np.where(bn_, KID, ck)
        cp_ = CP[np.maximum(ck, 0)]
        if BA_ON:   # late births: a choice to have a child of one's own starts one as fertility at that age allows
            cp_ = np.where(BIRTH_O[s, a], cp_ * np.where(female, fert(age, FERT_F), fert(age, FERT_M)), cp_)
        if BAT:   # a batch life event that starts a commitment is the match itself (falling in love, a child is born)
            cp_ = np.where((L["TIER"][s] == 1) & ((ck == CAR) | (ck == PAR) | (ck == KID) | (ck == COM)), 1.0, cp_)
        if CRS_ON:   # F16: any other act that would start one (a faith joined, a partner met in an everyday week) leans too
            cj_ = np.select([ck == PAR, ck == KID, ck == FAI], [0, 1, 2], -1)
            gate_ = (cj_ >= 0) & (CRS_EV[s] < 0)
            if gate_.any():
                cp_ = np.where(gate_, cp_ * np.minimum(1.0, course_q()[ar, np.maximum(cj_, 0)]), cp_)
        if PA_ON:   # F9: a first home together comes with adulthood
            cp_ = np.where(ck == PAR, cp_ * np.interp(age, PA_A, PA_F), cp_)
        ok_ = succ & ~idle
        if OR_ON and BORN_S_ >= 0:
            ok_ = ok_ | bn_
        fi = np.nonzero((ck >= 0) & ok_ & ~recon & (rng.random(N) < cp_))[0]
        fk = ck[fi]; new = ~held[fi, fk]
        if BAT:   # R15: a later child born (or taken in) while there are children already is one more living child
            kb_ = (ck == KID) & ok_ & ~recon & (L["TIER"][s] == 1) & kid_on
            alive[kb_, 5] += 1; kid_last[kb_] = t
            birth_log.extend((int(n), t, L["names"][s[n]], L["labels"][s[n]][a[n]]) for n in np.nonzero(kb_)[0])
        fi, fk = fi[new], fk[new]
        birth_log.extend((int(n), t, L["names"][s[n]], L["labels"][s[n]][a[n]]) for n in fi[fk == KID])
        held[fi, fk] = True; I[fi, fk] = 0.2; sat[fi, fk] = 0.6; since[fi, fk] = t
        if RE_ON:   # F8: going back to work, by their own pick, ends the retirement (one work status)
            retired[fi[fk == CAR]] = False
        # what a commitment expects of you: partly the way you entered it, partly who you were then, partly the
        # people and place it belongs to (a job or a partner brings their own ways)
        pm = P["commit_mix"]; prof[fi, fk] = pm[0] * ma[fi] + pm[1] * w[fi] + pm[2] * nic[fi]
        for n, kk in zip(fi, fk):
            commit_log.append((int(n), t, int(kk), "start", prof[n, kk].round(2).tolist(), 0.2))
            if n in events:
                events[n].append(dict(commitment=dict(age=round(age, 2), kind=KNAMES[kk], what="start",
                                                      through=L["labels"][s[n]][a[n]], profile=prof[n, kk].round(2).tolist())))
        # living a commitment: its own situations shape satisfaction and strength; holding it is an investment
        upd = (L["DOM"][s] >= 0.7) & held & (~idle)[:, None] & ~recon[:, None]
        sat = np.where(upd, sat + 0.05 * (succ[:, None] - sat), sat)
        I = np.where(upd, _uclip(I + np.where(succ[:, None], 0.02, -0.02), 0.05, 1), I)
        grow_ = held.copy()
        if age < P["faith_own_age"]:
            grow_[:, FAI] &= ~faith_given                   # the family's faith, not yet one's own
        I = np.where(grow_, I + P["invest"] * (1 - I), I)
        if len(ri):
            ch, ok = a[ri], succ[ri]
            sel = ch == 0                                    # recommit, and talk yourself back into it
            rs = ri[sel & ok]
            dy_ = P["rationalise"] * (centre(np.log(prof[rs, rkk[sel & ok]] + 0.02)) - y[rs])
            y[rs] += dy_; asrc[rs, 5] += dy_
            I[ri[sel], rkk[sel]] = _uclip(I[ri[sel], rkk[sel]] + np.where(ok[sel], 0.15, -0.05), 0.05, 1)
            sat[ri[sel & ok], rkk[sel & ok]] = 0.7
            sel = (ch == 1) & ok                             # reshape it toward the want
            prof[ri[sel], rkk[sel]] = 0.6 * prof[ri[sel], rkk[sel]] + 0.4 * m[ri[sel], 1]; sat[ri[sel], rkk[sel]] = 0.6
            clash_by[ri, rkk] = np.where(ch < 3, ch, clash_by[ri, rkk])
            sel = (ch == 2) & ok                             # walk away
            end(ri[sel], rkk[sel], "left", t)
            stress[ri[(ch == 2) & ~ok]] += 0.2
        # endings nobody chooses: retirement, widowhood (inside a bereavement), job loss (inside a betrayal)
        if P["retire_hz"] is None:                           # the old rule: from pension age, about two years on average
            ret = held[:, CAR] & (age >= P["retire_age"]) & (rng.random(N) < 0.01)
        else:                                                # early or late: health, means and fit decide who goes when
            ra_, rh_ = np.asarray(P["retire_hz"], float).T
            mx_ = P["retire_means"] * (1.0 if age < P["retire_age"] else 1 / 3)
            h_ = (np.interp(age, ra_, rh_) * np.exp(P["retire_health"] * (0.7 - res[:, HEA]))
                  * _uclip(res[:, MON] / 0.2, 0.25, 4.0) ** mx_ * (1 + P["retire_misfit"] * misfit[:, CAR]))
            ret = held[:, CAR] & (rng.random(N) < h_ / 52)
        if RE_ON:   # F8: a job just taken (back from retirement, or any) is not retired from in its first weeks
            ret = ret & (t - since[:, CAR] >= P["retire_back"])
        if RET_SEA:   # retiring opens the later-life season, whose first step is the last day at work
            ret = ret & (ret_pend < 0)
            for n in np.nonzero(ret & ~sea_had[:, ELD_])[0]:
                if sea_fits(ELD_, age):
                    sea_open(n, ELD_); ret_pend[n] = t; ret[n] = False
            ret_pend[(ret_pend >= 0) & ~held[:, CAR]] = -1
            late_ = (ret_pend >= 0) & (t - ret_pend > 8)          # the day never came as a moment: retired all the same
            ret = ret | late_; ret_pend[late_] = -1
        end(np.nonzero(ret)[0], [CAR] * int(ret.sum()), "retired", t)
        if P["faith_drift"] is not None and age >= P["faith_own_age"]:   # a faith or cause that quietly stops mattering
            fa_, fh_ = np.asarray(P["faith_drift"], float).T
            hf_ = (np.interp(age, fa_, fh_) * np.exp(P["faith_tilt_k"] * ((w - 1 / C) @ np.asarray(P["faith_tilt"], float)))
                   * _uclip(1.2 - I[:, FAI], 0.1, 1.2))
            dr_ = held[:, FAI] & ~recon & (rng.random(N) < hf_ / 52)
            drift_now[:] = dr_
            end(np.nonzero(dr_)[0], [FAI] * int(dr_.sum()), "left", t)
            drift_now[:] = False
        wid = WID_ON & held[:, PAR] & (rng.random(N) < 0.005 * np.exp((age - 55) / 10) / 52)   # partner dies (yearly risk 0.5% at 55, 6% at 80)
        widowed |= wid; hz_mem[wid] += P["hz_remind"] * HZ_ROLE[-1]
        need[wid, NIDX["belonging"]] -= 0.4; stress[wid] += 0.5
        if NW_ON: nw_mark(NW_LOSS)
        end(np.nonzero(wid)[0], [PAR] * int(wid.sum()), "widowed", t)
        # resources drift toward what a life's commitments and age provide
        mt = P["money_base"] + 0.45 * held[:, CAR] * (0.4 + 0.6 * I[:, CAR]) + P["pension_k"] * pension - P["kid_cost"] * kids
        if P["pension_base"] and age >= P["retire_age"]:   # F9: the state pension
            mt = mt + P["pension_base"]
        if LP_ON:   # F9.38: a new job's pay, drawn once (a change of employer draws again, rho of it the last job's)
            nj_ = np.nonzero(held[:, CAR] & (ago["job"] != lp_at))[0]
            if len(nj_):
                r_ = np.where(lp_at[nj_] == NEVER, 0.0, lp_rho)
                lp_z[nj_] = r_ * lp_z[nj_] * lp_d[nj_] + np.sqrt(1 - r_ ** 2) * lp_rng.standard_normal(len(nj_))
                lp_d[nj_] = 1.0; lp_at[nj_] = ago["job"][nj_]
                if PC_ is not None:   # F9.40: the colours lean the new job's pay and its spread
                    lc_ = 5 * w[nj_] - 1
                    lp_mu[nj_] = lc_ @ PC_[0]; lp_sc[nj_] = np.exp(lc_ @ PC_[1])
            sd_ = lp_sd * lp_sc * lp_d
            mt = mt + 0.45 * held[:, CAR] * (0.4 + 0.6 * I[:, CAR]) * (np.exp(lp_mu + sd_ * lp_z - sd_ ** 2 / 2) - 1)
            if P["pen_pay"] is not None and age >= 50:   # F9.38: a career's pension follows the pay of the last job
                ps_ = P["pen_pay"] * lp_sd * lp_sc
                mt = mt + P["pension_k"] * pension * (np.exp(lp_mu + ps_ * lp_z - ps_ ** 2 / 2) - 1)
            lp_d *= 0.5 ** (1 / (52 * lp_half))
        if PRP_ON and age >= 18:   # F9.38: a couple that lives together shares its money: a working partner's pay
            tog_ = r_has[:, CO_T_].any(1) if len(CO_T_) else held[:, PAR]
            if WON:   # the partner in the cast, at work
                ps_ = np.asarray(WL.PP.pslot); tog_ = tog_ & (ps_ >= 0) & np.asarray(WL.PP.emp)[np.arange(N), np.maximum(ps_, 0)]
            mt = mt + P["pair_pay"] * (tog_ & held[:, PAR])
        tt = 0.15 + 0.3 * held[:, PAR] + 0.15 * held[:, KID] + 0.25 * held[:, COM] + 0.1 * held[:, CAR]
        if HH_ON or TP_ON:   # F3: the household's money until they live on their own; ties are the people around them
            own_, away_ = home_share(age)
            if HH_ON:
                hh_lv_, hh_fl_ = household(age)
                mt = (1 - own_) * hh_lv_ + own_ * mt
            if TP_ON:
                tt = np.asarray(WL.PP.ties, float) if WON else ties_off(age, away_)
                if WON and P["tie_k"] != 1.0:   # F9: the people's closeness as ties, read on a scale (k = 20 / the T used)
                    tt = 1 - (1 - tt) ** (P["tie_k"] * (np.exp((5 * w - 1) @ TC_) if TC_ is not None else 1.0))
                if WON and P["kid_tie"] is not None and age < 15:   # F9.39: a child's ties are first its family's
                    tt = np.maximum(tt, P["kid_tie"])
        ht = _uclip(1 - 0.012 * max(0.0, age - 35), 0.2, 1)
        if MK_ON:   # spheres phase 2, the mark of the work: hard work ages the body (years beyond its own)
            ht = _uclip(ht - 0.012 * np.asarray(WL.PP.mark_wear, float), 0.2, 1)
        ft = FREE_STAGE[stage] - 0.1 * kids - 0.05 * held[:, PAR]
        if RON:   # a title's own resources: a nurse's pay, the freedom a record takes
            tr_ = (r_has[:, :NT_] * np.where(TK_ < NK, 0.4 + 0.6 * I[:, np.minimum(TK_, NK - 1)], 1.0)) @ GR["meets_res"]
            mt = mt + tr_[:, MON]; tt = tt + tr_[:, TIE]; ht = ht + tr_[:, HEA]; ft = ft + tr_[:, FRE]
        if WON:   # the world: rents, prices, the welfare floor, rights (package §5, Resources)
            wm_, wf_ = WL.resources(held[:, CAR]); mt = mt + wm_; ft = ft + wf_
            if WFX_ON:   # the money and freedom a life drifts to, by the world's cause
                rp_ = WL.resources_parts(held[:, CAR])
                wfx_track("money", {k_: rp_[k_] for k_ in ("housing", "prices", "welfare")}, age, dead)
                wfx_track("freedom", {"rights": rp_["rights"]}, age, dead)
            if WL2_ON:   # WL2: the small effects, each charged once (spheres-implementation.md "One cost, one place")
                w2_ = WL.wl2_parts(held[:, CAR])
                mt = mt + w2_["prices_work"] + w2_["recession"] + w2_["disaster"]
                ft = ft + w2_["rec_hours"] + w2_["disaster_time"]; tt = tt + w2_["pandemic"]
                if WFX_ON:
                    wfx_track("money", {k_: w2_[k_] for k_ in ("prices_work", "recession", "disaster")}, age, dead)
                    wfx_track("freedom", {k_: w2_[k_] for k_ in ("rec_hours", "disaster_time")}, age, dead)
                    wfx_track("ties", {"pandemic": w2_["pandemic"]}, age, dead)
        if DB_ON:   # phase 5: holdings yield, a home saves the rent, debts' payments take their share of income
            d_inc[:] = np.maximum(mt, 0.02)
            hm_ = (hk == 0).any(1)
            # a home of their own: .05, plus the rent a renter of that household would pay (world_link's "housing" read as
            # if own_home were false; for a life the world already charges, that charge ends), less the loan's payment
            rent_ = -0.05 * float(_uclip(WL.W.housing, -1, 1))
            mt = mt - rent_ * hm_ + 0.05 * hm_ + np.where(hk >= 0, H_YV[np.maximum(hk, 0)], 0.0).sum(1) * d_inc
            ds_ = np.where(dk >= 0, dsz / dterm + drate * dbal / 12, 0.0).sum(1)
            mt = mt * (1 - np.minimum(ds_, 0.9))
            pd_ = (WL.deaths()[:, 0] > 0) & (np.asarray(WL.PP.alive)[:, 0] == 0) & ~dead
            if H_OK[0] and age >= 16 and pd_.any():
                for n in np.nonzero(pd_)[0]:
                    db_inherit(n)
        if HH_ON:   # F3 D2: the family is a floor in hard times, by its class and how close a living parent is
            mt = np.maximum(mt, P["hh_floor"] * hh_fl_)
        tie_r = 0.01
        if LON_ON and age >= LA_[0]:   # F9.39: a spell of loneliness starts or ends; while it lasts the ties fall away
            rk_ = (LO_["single"] * ~held[:, PAR] + LO_["work"] * (~held[:, CAR] & ~retired & (ago["job"] != NEVER)) * (age < P["retire_age"])
                   + LO_["low"] * (md_end[:, 0] > t) + LO_["ill"] * (bd_cw.sum(1) > 0))
            u_ = lon_rng.random(N)
            on_ = ~lone & ~dead & (u_ < float(np.interp(age, LA_, LF_)) * np.exp(rk_) / 52)
            lone = (lone | on_) & ~(lone & (u_ < LO_["out"] * np.exp(-0.5 * rk_) / 52))
            tt = np.where(lone, LO_["keep"] * tt, tt); tie_r = np.where(lone, LO_["rate"], 0.01)
        mon_r = P["mon_drift"]
        if P["job_gap"] is not None and age >= 18 and age < P["retire_age"]:   # F9.38: a lost wage stops at once
            gp_ = (~held[:, CAR] & ~retired & (ago["job"] != NEVER) & (end_t[:, CAR] > NEVER // 2)
                   & (t - end_t[:, CAR] < 52 * P["job_gap"][2]))
            mt = mt - P["job_gap"][0] * gp_
            mon_r = np.where(gp_ & (mt < res[:, MON]), P["job_gap"][1], P["mon_drift"])
        if NET_ON:   # F9.38: a long hard spell meets help (benefits, family, a way out): after net_y years with the money
            net_m += (res[:, MON] - net_m) / 13          # over a season at 5% or less (a loan's or a good week's brief lift
            lo_w = np.where(net_m <= 0.05, lo_w + 1, 0)  # does not end the spell), net_d years of at least net_lv
            st_ = (lo_w >= 52 * net_y) & (age >= 18)   # (an adult's: a child's money is the household's)
            net_t = np.where(st_, t + int(52 * net_d), net_t); lo_w[st_] = 0
            net_ = net_t > t
            mt = np.where(net_, np.maximum(mt, net_lv), mt)
            if P["job_gap"] is not None and age >= 18 and age < P["retire_age"]:
                mon_r = np.where(net_, P["mon_drift"], mon_r)
        res[:, MON] += mon_r * (mt - res[:, MON]); res[:, TIE] += tie_r * (tt - res[:, TIE])
        if DB_ON and t % 4 == 0 and age >= 18:
            db_month()
        if NET_ON:
            res[:, MON] = np.where(net_, np.maximum(res[:, MON], net_lv), res[:, MON])
        if HM_ON:   # v22.5 F1: the body and the mind make health (ht's age part is the body's own curve there)
            body_week(ht, _uclip(1 - 0.012 * max(0.0, age - 35), 0.2, 1))
        else:
            res[:, HEA] += 0.01 * (ht - res[:, HEA])
        res[:, FRE] += 0.02 * (ft - res[:, FRE])
        res[:, HEA] -= 0.08 * ((stakes >= 1.3) & ~succ & ~idle)       # disasters that go wrong hurt the body
        if SHON:   # shadows: rigid and ruthless lose people, reckless burns bridges and the body pays, rigid strains on duty
            res[:, TIE] -= 0.01 * P["sh_tie"] * (shA[:, 0] + shA[:, 2] + 0.5 * shA[:, 3])
            res[:, HEA] -= 0.01 * P["sh_body"] * shA[:, 3]
            stress += P["sh_strain"] * shA[:, 0]
            dsc -= P["sh_burn"] / 52 * shA[:, 3] * (dsc - P["disc_range"][0])
            # the four sources (shadows-mechanics.md §3), each 0 to 1
            a_w_ = softmax(y)
            sh_src[:, :, 0] = _uclip(2.5 * (hold - 0.2), 0, 1) * _uclip(5 * (w - a_w_), 0, 1) \
                * _uclip((t - sh_brk) / 52.0, 0, 1)[:, None]                 # holding on (a breakthrough lets go for a while)
            sh_src[:, :, 1] = _uclip((w - 0.30) / 0.30, 0, 1)                   # ruling
            en_max_ = np.where(ENEMY_B[None], w[:, None, :], 0.0).max(2)       # the stronger of its two enemies
            sh_src[:, :, 2] = _uclip((0.12 - en_max_) / 0.09, 0, 1)             # no counterweight
            sh_src[:, :, 3] = _uclip(stress / 1.5 + Q / 4, 0, 1)[:, None] * w / w.max(1, keepdims=True)   # strain
            sk_ = np.asarray(P["sh_src"], float)
            tgt_ = 1 - np.prod(1 - sk_[None, None] * sh_src, 2)
            if SHAR_ON and getattr(WL.PP, "sh_around", None) is not None:   # phase 5: the shadow around them (N5)
                sa_ = _uclip((np.asarray(WL.PP.sh_around, float)[:, np.argsort(WL.W.perm)] - 0.1) / 0.4, 0, 1)
                tgt_ = 1 - (1 - tgt_) * (1 - P["sh_around"] * sa_)
            if LW_ON:   # S7: years leading one way add to that colour's shadow part (People.lead_sh, 0 .. lead_par sh)
                tgt_ = 1 - (1 - tgt_) * (1 - np.asarray(WL.PP.lead_sh, float)[:, np.argsort(WL.W.perm)])
            sup_ = np.clip(0.5 * (need[:, NIDX["belonging"]] + res[:, TIE]), 0, 1)
            integ_ = np.where(ENEMY_B[None], J, 0.0).max(2)                    # an enemy pair held well
            tgt_ = tgt_ * (1 - P["sh_care"] * sup_)[:, None] * (1 - P["sh_integ"] * integ_) * (age >= P["sh_age"])
            tgt_ = np.clip(tgt_ * SHG_[None], 0, 1)
            up_ = tgt_ > shS                                                   # shadows come faster than they go
            shS += (tgt_ - shS) / (4.33 * np.where(up_, P["sh_grow"], P["sh_fade"]))
            if pausing and not recon.all():   # the Voice leads them out: the shadow pulled the character's own pick, the
                # player picked another way, and it worked
                ctr_ = (a != a_self) & succ & ~idle & ~recon
                for n in np.nonzero(ctr_)[0]:
                    pu_ = shA[n] * m[n, a_self[n]]
                    c_ = int(pu_.argmax())
                    if pu_[c_] > 0 and m[n, a[n], c_] < m[n, a_self[n], c_]:
                        shS[n, c_] = max(0.0, shS[n, c_] - P["sh_counter"])
            rf_ = SH_REFL[s]                                                   # a reflection moment met: they see it
            for n in np.nonzero((rf_ >= 0) & ~recon)[0]:
                c_ = int(rf_[n]); shS[n, c_] = max(0.0, shS[n, c_] - P["sh_seen"]); sh_seen[n, c_] = True; sh_rt[n, c_] = t
            shA = np.minimum(1.0, w * shS / P["sh_full"])
        res = _uclip(res, 0, 1)
        # clash: holding a commitment that no longer fits what you want. It costs stress until it is resolved
        mis = _uclip(1 - 5 * (prof * softmax(y)[:, None, :]).sum(-1), 0, 1)
        on = held & (clash0 < 0) & (mis > P["clash_on"])
        clash0[on] = t; clashI[on] = I[on]; clash_by[on] = -1
        cload = (held * (clash0 >= 0) * mis * I).sum(1)         # living against what you are supposed to be (ought conflict)
        stress += P["clash_stress"] * cload
        done = (clash0 >= 0) & (~held | (mis < P["clash_off"]))
        for n, kk in zip(*np.nonzero(done)):
            how = "left" if not held[n, kk] and clash_by[n, kk] == 2 else "ended otherwise" if not held[n, kk] else \
                  {0: "doubled down", 1: "reshaped it"}.get(int(clash_by[n, kk]), "made peace")
            clash_log.append((int(n), int(kk), int(clash0[n, kk]), t, how, round(float(clashI[n, kk]), 2), int(np.argmax(softmax(z[n])))))
            if n in events:
                events[n].append(dict(clash=dict(kind=KNAMES[kk], start=round(clash0[n, kk] / 52, 1), end=round(age, 1), how=how)))
        clash0[done] = -1

        # ---- 3c. v7 goals: steps taken, strength, meaningful success, plans reached
        if GON:
            ra = rel[ar, :, a]                                       # N,G: how far this week's act served each goal
            acted = (~idle)[:, None] & (gk >= 0) & (ra > 0)
            win_ = acted & succ[:, None]; fail_ = acted & ~succ[:, None]
            st_ = np.minimum(stakes, 1.2)[:, None]
            gs = np.where(win_, gs + np.where(gk == 0, P["g_up_dream"], P["g_up"]) * ra * st_ * (1 - gs), gs)
            gs = np.where(fail_, gs - P["g_down"] * ra * st_ * (1.5 - outlook)[:, None] * gs, gs)
            gpk = np.maximum(gpk, gs)
            glast = np.where(acted, t, glast)
            # tries that work and feel like one's own gather toward a passion (2A)
            own_g = 0.5 * (w + softmax(y))
            conc_a = _uclip(2 * (ma * own_g).sum(1) / own_g.max(1) - 1, -0.5, 1)
            # only real tries count: an act clearly in its ways, in a moment that mattered, that felt like one's own
            dv = win_ * (gk <= 1) * (ra >= 0.5) * ra * _uclip((stakes - 0.4) / 0.4, 0, 1)[:, None] * np.maximum(conc_a, 0)[:, None]
            gv = gv + dv
            # taken in freely or under pressure? Parents prizing it (childhood), needing it for one's worth, being only about
            # this one thing, against support and room to choose (Mageau et al. 2009): harmonious or obsessive passion
            lk_ = np.maximum(0, P["need_set"] - need) / P["need_set"]
            dp_ = (gk <= 1) * (gk >= 0) * gs; spec = dp_ / np.maximum(dp_.sum(1, keepdims=True), 1e-9)
            ctl = (P["ctl_fam"] * _uclip(5 * np.einsum("nc,ngc->ng", fam, gm) - 1, 0, 2) * (stage <= 1)[:, None]
                   + P["ctl_lack"] * 0.5 * (lk_[:, NIDX["competence"]] + lk_[:, NIDX["meaning"]])[:, None] + P["ctl_spec"] * spec
                   - P["ctl_sup"] * (support - 0.5)[:, None] - P["ctl_free"] * (res[:, FRE] - 0.5)[:, None]
                   + P["ctl_stress"] * (stress - 0.5)[:, None] + P["ctl_press"] * (0.5 * np.abs(nic - w).sum(1) - 0.15)[:, None]
                   + P["ctl_react"] * (react - 1)[:, None])
            auto_now = 1 / (1 + np.exp(-(P["ctl_mid"] - 4 * ctl)))   # stress and pressure to be someone else make it compulsive
            ga = np.where(dv > 0, ga + 0.5 * dv / (1 + gv) * (auto_now - ga), ga)   # set while it is taken in, then settles
            # a passion lived lifts the mood when harmonious, much less when obsessive (Vallerand et al. 2003)
            mood = mood + P["hp_mood"] * (((gk == 1) & win_) * gs * ra * (ga - 0.5 * (1 - ga))).sum(1)
            # plans: progress and what has been put in
            pln = gk == 2
            # a pursuit moves on deliberate steps: they take self-control and free time (busy, stressed weeks get less done)
            gp = np.where(pln & win_ & (gd < 0), gp + ra * st_ * (ctrl * (0.3 + 0.7 * res[:, TIM]))[:, None]
                          / np.asarray(P["g_size"], float)[ghz], gp)
            gp = np.where(pln & win_ & (gd >= 0), np.minimum(0.95, gp + 0.1 * ra), gp)
            gi = np.where(pln, gi + 0.005 * gs + 0.05 * acted * st_, gi)
            # what the person learns about their chances: how often one comes, and how a step looks to them
            chance = (rel >= 0.5).any(2)
            gch = np.where(pln, gch * (1 - 1 / 52) + chance / 52, gch)
            gph = np.where(pln & chance, 0.9 * gph + 0.1 * np.where(rel >= 0.5, p_hat[:, None, :], 0).max(2), gph)
            # reached: the steps add up, or the commitment the plan was for begins
            newk = held & ~held_wk
            got = pln & (gtt < 0) & (((gd < 0) & (gp >= 1)) | ((gd >= 0) & newk[ar[:, None], np.maximum(gd, 0)]))
            if RON:   # a plan aimed at a title is reached when the title is held
                got |= pln & (gtt >= 0) & r_has[ar[:, None], np.maximum(gtt, 0)]
            for n, j in zip(*np.nonzero(got)):
                cc = float(_uclip(2 * (gm[n, j] * own_g[n]).sum() / own_g[n].max() - 1, -0.5, 1))
                fit_ = 0.5 + 0.5 * max(cc, 0)    # reaching what fits who one is means more (Sheldon & Elliot 1999)
                need[n, NIDX["meaning"]] += 0.15 * gs[n, j] * fit_; need[n, NIDX["competence"]] += 0.1 * gs[n, j]
                if NW_ON: nw_mark(NW_GOAL)
                mood[n] += 0.3 * gs[n, j] * fit_
                outlook[n] += 0.1 * (1 - outlook[n]) * TON; steady[n] += 0.05 * fit_ * TON
                if gpar[n, j] >= 0:
                    gs[n, gpar[n, j]] = min(1.0, gs[n, gpar[n, j]] + 0.1)
                gp[n, j] = 1.0
                end_goal(n, j, "achieved")

        if AIM_ON:   # aims v1: a spark moment's try, seal or drop
            aim_spark()
