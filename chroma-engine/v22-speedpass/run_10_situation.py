# run_10_situation.py: part 10 of 18 of engine._run, the life loop.
# 1. the situation: the gates, the draw, the "situation" pause; commitments reconsidered; goal fit.
# Lines here are _run's own, unchanged and at their own indent: engine.py joins the parts in order (engine.RUN_PARTS)
# and compiles them as one, so a name used here may be set in an earlier part. Never import or run it alone.
        # ---- 1. situation: unlocked by life stage, weighted toward what your niche brings
        # gate: everything but the life stage (the age window, needs and excludes, and in a batch its conditions)
        gate = (((age >= L["AGE"][:, 0]) & (age <= L["AGE"][:, 1])) | (not P["age_windows"]))[None]
        nk_, ek_ = L["NEEDK"], L["EXCLK"]                     # situations that need, or exclude, a commitment
        excl = held.copy(); excl[:, CAR] |= retired                # no new career after retiring
        gate = gate & ((nk_ < 0)[None] | held[:, np.maximum(nk_, 0)]) & ((ek_ < 0)[None] | ~excl[:, np.maximum(ek_, 0)])
        if RE_ON:   # F8: retired and not working, the work moments no longer come (the doors back stay)
            gate = gate & ~((retired & ~held[:, CAR])[:, None] & WORK_S[None])
        avail = L["STG"][:, stage].T & gate                   # N,S: stage and gate
        if BAT:   # batch: once per life (or per commitment), the condition holds, the one who would die is alive
            avail0 = avail
            gate = gate & cond_ok & ~once_done[:, ROOT]
            if SH_ON:
                gate[:, SH_I] &= SH_EL
            if INMS_ON_:   # part 4: open only with an active former-inmate tie
                gate[:, INMS_] &= pt_act[:, None]
            if RON:   # a moment only someone holding a title or perk meets (a nurse's night shift): any of its holds:, and
                # with tenure: only while one of them has been held that many years (Emren's point 6: new, settled, senior)
                if HOLDS_.size:
                    gate[:, HOLDS_] &= (r_has[:, HOLD_C].astype(np.float32) @ HOLDM_C) > 0
                if TENS_:   # speed pass: the same test for every tenure moment at once (then the loop's last values)
                    y_ = (t - r_since[:, TEN_I]) / 52
                    gate[:, TEN_S] &= np.logical_or.reduceat(r_has[:, TEN_I] & (y_ >= TEN_LO) & (y_ <= TEN_HI), TEN_ST, axis=1)
                    s_, ii_, lo_, hi_ = TENS_[-1]; y_ = (t - r_since[:, ii_]) / 52
            if AQ_ON:   # v7: a moment that comes only to someone in a state (a wealthy person's advisor calls)
                gate &= (L["ADJ_SREQ"] < 0)[None] | adj[:, np.maximum(L["ADJ_SREQ"], 0)]
            if WON:   # a cast death this week (or one waiting for its moment) still opens its moment: the cast counted it already
                dth_ = (WL.deaths()[:, :5] > 0) | dq_
                if OR_ON:   # F7, one roll of the living: a death in the cast is the world's, so its moment comes only then
                    gate[:, KL_] &= np.concatenate([dth_, alive[:, 5:6] > 0], 1)[:, KILLS[KL_]]
                else:
                    gate[:, KL_] &= (alive[:, KILLS[KL_]] > 0) | np.concatenate([dth_, np.zeros((N, 1), bool)], 1)[:, KILLS[KL_]]
            else:
                gate[:, KL_] &= alive[:, KILLS[KL_]] > 0
            if BA_ON and BF_ON:   # birth_free: each own-birth moment at least a year after the last child
                gate[:, BIRTH_S] &= ((t - kid_last) >= 52)[:, None]
            if NE_ON:   # F9.5: the children leave home once the youngest is grown
                gate[:, NE_S] &= ((t - kid_last) >= NE_A * 52)[:, None]
            if BORN_S_ >= 0:   # F7: the moment a child is born is a birth, at least a year after the last one
                gate[:, BORN_S_] &= (t - kid_last) >= 52
            gate[:, INNER_] &= (t - sit_last[:, INNER_]) >= P["inner_gap"]
            if len(TRG_S_):   # body_trust's gate (trust: <sphere> low|high): under the gate's low or over its high; never
                if BT_ON:      # with body_trust off or the world off, or before the life's trust starts at 15
                    f_ = btrust[:, TRG_[TRG_S_, 0]]
                    gate[:, TRG_S_] &= np.where(TRG_[TRG_S_, 1] == 0, f_ < BT_G["low"], f_ > BT_G["high"])
                else:
                    gate[:, TRG_S_] = False
            if SEA_ON:
                gate_sea = gate.copy()                         # for the season's own moments, before they are kept out
                gate[:, TH_ANY] = False                       # a season's moments come only in its season
            avail = L["STG"][:, stage].T & gate
        aff = np.exp(2.0 * ((RX.seek_draw_mix(nic) if SK_ON else nic) @ L["ALPHA"].T)) * avail * RATE[None] * (1 + P["dom_freq"] * (held * I) @ L["DOM"].T)   # seek: (1 - k) surroundings + k attraction
        if SACS_ON_:   # S5: a sacred line's moments come only with an offer (or a wound) of the life's own
            aff[:, SACS_] = 0.0
        if BAT:
            aff = aff * cond_fac
        if WON:   # the world: time of year, holy days, the place's features, the settings one is in, the technology there is
            mf_ = WL.moment_factor(age, sit_last); aff = aff * mf_
        if FARS_ON_:   # far_ties: a far moment comes only with a tie's call (forced), never by the everyday draw
            aff[:, FARS_] = 0.0
        if EYEW_ON_:   # S3, S4: a caught-between or odd-one-out moment comes only by the place reading
            aff[:, EYEW_] = 0.0
        if LEADS_ON_:   # lead_ways (S7): a post's moment comes only with the post (forced), never by the everyday draw
            aff[:, LEADS_] = 0.0
        if PTW_ON_:   # place_turnover: a place moment comes only with its closing or opening (forced)
            aff[:, PTW_] = 0.0
        if WAW_ON_:   # the world answers: an ask, a decision or a figure's moment comes only when the world brings it
            aff[:, WAW_] = 0.0
        if WO_ON:   # F10: a world moment only on the world's event; one waiting for the world keeps its gap:
            aff[:, WMZ_] = 0.0
            if len(WG_I):
                aff[:, WG_I] = aff[:, WG_I] * _uclip(((t - sit_last[:, WG_I]) / 52 - WGLO_) / WGW_, 0, 1)
        aff_open = aff                                 # the moments open to the person, before their pause
        if GAPXON_:   # gap: on an everyday or inner moment
            gapw_ = np.ones(sit_last.shape)   # speed pass: the ramp on the gapped moments' columns only (1 elsewhere, as before)
            gapw_[:, GAPX_I] = _uclip(((t - sit_last[:, GAPX_I]) / 52 - GAPXLO_[:, GAPX_I]) / GAPXW_[:, GAPX_I], 0, 1)
            aff = aff * gapw_
        if SHON:   # G stuck in their ways: moments that could start something new come less often
            sdr_ = 1 - P["sh_door"] * shA[:, 4][:, None] * SH_NEW[None]
            aff = aff * sdr_
        if DTH_ON and (dl_at > NEVER // 2).any():   # v22.5 F2: in a last decline nothing new begins
            aff = aff * np.where((dl_at > NEVER // 2)[:, None], 1 - 0.95 * SH_NEW[None], 1.0)
        seekE = 1.0 if not SHON else sdr_
        if GON:   # v7: plans (and a little, passions) make people seek chances for them; a domain plan seeks its life events
            aff = aff * (1 + P["g_seek"] * np.einsum("ng,ngs->ns", gs * np.where(gk == 2, 1.0, np.where(gk == 1, 0.5, 0.0)), gsr))
            seekE = seekE * (1 + P["g_seek_ev"] * np.einsum("ng,ngs->ns", gs * ((gk == 2) & (gd >= 0)), gsr))
        if AIM_ON:   # aims v1: the moments with a way into each aim's next step, and a player's aim's spark moment
            ap_ = spark_gate(1 + AP_["seek"] * aim_pull())
            aff = aff * ap_; seekE = seekE * ap_
        if P["base_rates"]:
            # v6: life events come at their real yearly rates; every other week is ordinary life (an everyday situation)
            # the outside context moves each kind of event: family, resources, the era, the world
            X = np.stack([held[:, PAR] + held[:, KID] + 0.5 * held[:, COM] - 1.0,
                          (np.asarray(WL.PP.ties, float) if WON and not TP_ON else res[:, TIE]) - 0.5, res[:, MON] - 0.5,
                          res[:, HEA] - 0.5, np.full(N, era_i[t]), np.broadcast_to(drv_h, (N,)), np.full(N, drv_u),
                          np.full(N, drv_p), held[:, COM] * I[:, COM] + (np.asarray(WL.PP.community, float) if WON else 0.0),
                          _uclip(stress - 0.5, -0.5, 1.0), np.minimum(trouble, 2.0), np.minimum(fortune, 2.0)], 1)
            if GAPON_:   # the Library's gap: lo-hi (speed pass: each column computed once, by the rule that keeps it)
                refr = np.empty(ev_last.shape)
                refr[:, GAPN_I] = 1 - np.exp(-(t - ev_last[:, GAPN_I]) / (52 * P["ev_refr"]))
                refr[:, GAPM_I] = _uclip(((t - ev_last[:, GAPM_I]) / 52 - GAPLO_[:, GAPM_I]) / GAPW_[:, GAPM_I], 0, 1)
            else:
                refr = 1 - np.exp(-(t - ev_last) / (52 * P["ev_refr"]))
            xd_ = np.exp(X @ DRV.T)   # speed pass: computed once, used twice (the same numbers)
            ev_p = PERY[:, stage].T * avail * P["event_scale"] / 52 * ev_pm * xd_ * refr * seekE   # N,S
            if BA_ON and BF_ON:   # F9: a life's own births by its age, not its stage (the age window is in the gate)
                ev_p[:, BIRTH_S] = (BF_P * np.broadcast_to(gate, ev_p.shape)[:, BIRTH_S] * P["event_scale"] / 52
                                    * np.broadcast_to(ev_pm, ev_p.shape)[:, BIRTH_S] * xd_[:, BIRTH_S] * refr[:, BIRTH_S]
                                    * np.broadcast_to(seekE, ev_p.shape)[:, BIRTH_S])
            if AF_ON:   # F9: these life events by age, not the life stage reached (the age window is in the gate)
                ev_p[:, AF_S] = (AF_P * np.broadcast_to(gate, ev_p.shape)[:, AF_S] * P["event_scale"] / 52
                                 * np.broadcast_to(ev_pm, ev_p.shape)[:, AF_S] * xd_[:, AF_S] * refr[:, AF_S]
                                 * np.broadcast_to(seekE, ev_p.shape)[:, AF_S])
            if NE_ON:   # F9.5: by the youngest's age (in the gate), not the life stage reached
                ev_p[:, NE_S] = (NE_R * np.broadcast_to(gate, ev_p.shape)[:, NE_S] * P["event_scale"] / 52
                                 * np.broadcast_to(ev_pm, ev_p.shape)[:, NE_S] * xd_[:, NE_S] * refr[:, NE_S]
                                 * np.broadcast_to(seekE, ev_p.shape)[:, NE_S])
            if AR_ON:   # F9.24: these by age, between the stages' rates (the age window is in the gate)
                ev_p[:, AR_S] = (np.array([np.interp(age, x_, r_) for x_, r_ in AR_P])[None] * np.broadcast_to(gate, ev_p.shape)[:, AR_S]
                                 * P["event_scale"] / 52 * np.broadcast_to(ev_pm, ev_p.shape)[:, AR_S] * xd_[:, AR_S] * refr[:, AR_S]
                                 * np.broadcast_to(seekE, ev_p.shape)[:, AR_S])
            if BAT:   # how much the drivers raise each event's rate on average among those it can happen to (for DRV_NORM)
                el_ = avail & (PERY[:, stage].T > 0)
                drv_sum += (xd_ * el_).sum(0); drv_cnt += el_.sum(0)
                if DS_ON:   # F9: the drivers choose who, not how many, also with the world on and the v22.5 means: each
                    # life event's rate over its drivers' mean so far in this run (the norm its per_year already took out)
                    ev_p = ev_p * np.where(drv_cnt > 0, DRVN_ / np.maximum(drv_sum / np.maximum(drv_cnt, 1), 1e-9), 1.0)[None]
            if BAT:
                ev_p = ev_p * cond_fac             # the engine's likelier / rarer reading of a life event (1 when it has none)
            if CRS_ON:   # F16: the life events that start a partnership, a child, a faith come at each life's own lean
                crq_ = course_q(); cev_ = CRS_EV >= 0                # (a child's at it whether or not they hold one)
                cm_ = crq_[:, np.maximum(CRS_EV[cev_], 0)]
                cm_ = np.where(held[:, CRS_KS[np.maximum(CRS_EV[cev_], 0)]] & (CRS_EV[cev_] != 1)[None], 1.0, cm_)
                ev_p[:, cev_] *= cm_
            if BA_ON and P["birth_par"] is not None:   # F9.3: by the children already living
                bp_ = np.asarray(P["birth_par"], float)
                ev_p[:, BIRTH_S] *= bp_[np.minimum(alive[:, 5].astype(int), len(bp_) - 1)][:, None]
            if BW_ON:   # F9.2: by the partnership (none, a partner not living together, a home together)
                hm_ = held[:, PAR] & (r_has[:, BW_I].any(1) if BW_I else True)
                hm_t = np.where(hm_, np.minimum(hm_t, t), 10 ** 9)
                bwr_ = _uclip((t - np.where(hm_, hm_t, since[:, PAR])) / (52 * BW_[3]), 0, 1) if BW_[3] > 0 else 1.0
                ev_p[:, BIRTH_S] *= np.where(hm_, BW_[2] * bwr_, np.where(held[:, PAR], BW_[1] * bwr_, BW_[0]))[:, None]
            if BA_ON:   # late births: a life's own births by its age and sex
                ev_p[:, BIRTH_S] *= P["birth_k"] * np.where(female[:, None], fert(age, FERT_F) / BA_NF[None],
                                                            fert(age, FERT_M) / BA_NM[None])
            if BAT:   # deaths come at the rate of the age of those still alive (engine-owned; the Library's window still gates)
                qd_ = np.repeat(np.minimum(1, P["mort"][0] * np.exp(P["mort"][1] * (age + KILL_OFF[KILLS[KL_]])))[None], N, 0)
                if KCH_.any():   # R15: the children's own ages (the first child's years, less a little for the younger ones)
                    ca_ = np.maximum((t - since[:, KID]) / 52 - 1.5, 0)
                    qc_ = np.maximum(P["mort"][0] * np.exp(P["mort"][1] * ca_), P["kid_mort"]) + P["infant_mort"] * (t - kid_last < 52)
                    qd_[:, KCH_] = np.minimum(qc_, 1)[:, None]
                ev_p[:, KL_] = ((1 - (1 - qd_) ** alive[:, KILLS[KL_]]) * avail[:, KL_] * P["event_scale"] / 52 * ev_pm[:, KL_]
                                * np.exp(X @ DRV[KL_].T) * refr[:, KL_])
                if KCH_.any() and P["child_norm"]:   # C-X5: each child at their own age (the first child's years, each later
                    kc_ = np.nonzero(KL_)[0][KCH_]   # one about child_gap younger), a baby's first year once, and not raised by
                    a1_ = (t - since[:, KID]) / 52; nk_ = alive[:, KILLS[kc_[0]]]   # the event scale or one's spread (the
                    sv_ = 1 - P["infant_mort"] * (t - kid_last < 52)                # drivers still choose whose child)
                    for j_ in range(int(nk_.max(initial=0))):
                        q_ = np.maximum(P["child_mort"] * np.exp(P["mort"][1] * np.maximum(a1_ - P["child_gap"] * j_, 0)), P["kid_mort"])
                        sv_ = sv_ * np.where(nk_ > j_, 1 - np.minimum(q_, 1), 1.0)
                    ev_p[:, kc_] = ((1 - sv_) * (nk_ > 0))[:, None] * avail[:, kc_] / 52 * np.exp(X @ DRV[kc_].T) * refr[:, kc_]
            if WON:   # the world: each life event's rate by season, place, medicine and war (W.rate_mult), gated as above;
                # the world's own events, a cast member's ripe want and a death in the cast bring their moments (the
                # cast's deaths replace the engine's draw of them, but a child's, which the engine still keeps)
                rf_w = WL.rate_factor(sec_w if RON else np.full(N, -1))
                ev_p = ev_p * rf_w * mf_ * WL.channel_rates()   # and contagion, move wish
                ev_p[:, KL_ & ~KCHILD_] = 0.0
                frc_ = WL.fire_now.copy(); fdd_ = np.zeros_like(frc_); dfr_ = []
                if BA_ON and frc_[:, BIRTH_S].any():   # a birth the world brings comes by the same age and sex
                    frc_[:, BIRTH_S] &= (ba_rng.random(N) < np.where(female, fert(age, FERT_F), fert(age, FERT_M)))[:, None]
                for r_ in range(5):
                    for n in np.nonzero(dth_[:, r_])[0]:
                        ks_ = np.nonzero((KILLS == r_) & avail[n])[0]
                        si_ = int(ks_[WL.PP.rng.integers(len(ks_))]) if len(ks_) else -1
                        if si_ >= 0:
                            frc_[n, si_] = True; fdd_[n, si_] = True
                        dfr_.append((int(n), r_, si_))
                fok_ = avail
                if getattr(WL, "wa_pend", None):   # a decision the world brings a Known life comes at any stage, retired or
                    fok_ = avail.copy()            # not: their standing is its gate (a late rite or a pension closed it)
                    for n_ in WL.wa_pend:
                        fok_[n_, WL.pending[n_][2]] = True
                frc_ &= fok_; fdd_ &= avail
                if CRS_ON and frc_[:, cev_].any():   # F16: a match or a birth the world brings, at the same lean (as a chance)
                    frc_[:, cev_] &= crs_rng.random(frc_[:, cev_].shape) < cm_
                if WO_ON:   # F10: a world moment is not brought again inside its own gap: (once means once)
                    frc_[:, WMZ_] &= refr[:, WMZ_] > 0
            if FARS_ON_:
                ev_p[:, FARS_] = 0.0
            if EYEW_ON_:
                ev_p[:, EYEW_] = 0.0
            if LEADS_ON_:
                ev_p[:, LEADS_] = 0.0
            if SACS_ON_:
                ev_p[:, SACS_] = 0.0
            if PTW_ON_:
                ev_p[:, PTW_] = 0.0
            if WAW_ON_:
                ev_p[:, WAW_] = 0.0
            if BL_ON:   # v22.5 F1: the body's own risks (constitution, habits, strain, money) reach its moments in the Library
                bk_ = np.minimum(np.exp(BP_["risk_k"] * (np.interp(age, BAGE_X, BAGE_Y) - body_v)), 2.0)
                if P["risk_norm"]:   # F9: the risks choose who, the Library's rates how many (the living's mean is 1)
                    bk_ = bk_ / max(float(bk_[~dead].mean()) if (~dead).any() else 1.0, 1e-9)
                ev_p[:, BL_S] *= bk_[:, None]
            if ML_ON:   # and the mind's, less with resilience
                mk_ = np.minimum(np.exp(MP_["risk_k"] * (0.75 - mind_v)), 3.0) * (1 - md_res)
                if P["risk_norm"]:
                    mk_ = mk_ / max(float(mk_[~dead].mean()) if (~dead).any() else 1.0, 1e-9)
                ev_p[:, ML_S] *= mk_[:, None]
            if DTH_ON and (dl_at > NEVER // 2).any():   # F2: in a last decline nothing new begins
                ev_p = ev_p * np.where((dl_at > NEVER // 2)[:, None], 1 - SH_NEW[None], 1.0)
            fire = rng.random(ev_p.shape) < ev_p
            if WON:
                fire |= frc_
            if dead.any():
                fire &= ~dead[:, None]
            had_ev = fire.any(1)
            s_ev = np.argmax(np.where(fire, rng.random(ev_p.shape) + (2.0 * frc_ + 1.0 * fdd_ if WON else 0.0), -1.0), 1)
            if WON:   # a death in the cast brings its moment (first among the world's moments); if none is open, it waits up
                # to eight weeks for one, and only then grieves without it
                for n, r_, si_ in dfr_:
                    if si_ >= 0 and had_ev[n] and s_ev[n] == si_ and not dead[n]:
                        dq_[n, r_] = False
                        continue
                    if not dq_[n, r_]:
                        dq_[n, r_] = True; dq_t[n, r_] = t
                    if not dead[n] and t - dq_t[n, r_] < 8:
                        continue
                    dq_[n, r_] = False
                    need[n, NIDX["belonging"]] -= KILL_HIT[r_, 0]; stress[n] += KILL_HIT[r_, 1]
                    if NW_ON: nw_mark(NW_LOSS)
                    hz_mem[n] += P["hz_remind"] * HZ_ROLE[r_]; ago["death"][n] = t; ago["loss"][n] = t
                    if r_ == ROLES.index("partner") and held[n, PAR]:
                        widowed[n] = True; end([n], [PAR], "widowed", t)
                    if n in events:
                        events[n].append(dict(death=dict(age=round(age, 2), role=ROLES[r_], left=int(WL.PP.alive[n, r_]))))
            ev_last[had_ev, s_ev[had_ev]] = t
            if WFX_ON:   # a life event the world brought (its event) or made likelier or rarer (its rate), when it comes
                for n in np.nonzero(had_ev & ~dead)[0]:
                    si_ = int(s_ev[n])
                    if frc_[n, si_]:
                        e_ = WL.fire_why.get(si_)
                        if e_ is not None and not fdd_[n, si_] and WL.pending.get(int(n), (0, 0, -1))[2] != si_:
                            wfx_add(n, e_.get("kind"), "moment", 1.0, age, moment=L["names"][si_],
                                    cause=dict(domain=e_.get("domain"), kind=e_.get("kind"), key=e_.get("key"), age=round(age, 2)))
                    elif WL.rk[si_] >= 0 and WLM.RK[WL.rk[si_]] != "birth" and abs(rf_w[n, si_] - 1) >= 0.1:
                        rk_ = WLM.RK[WL.rk[si_]]; m_ = float(rf_w[n, si_])
                        wfx_add(n, "unemployment" if rk_ == "jobloss" else rk_, WFX_RISK[rk_], m_ - 1, age,
                                moment=L["names"][si_], share=round(max(0.0, 1 - 1 / m_), 3))
            if P["ev_gap"]:   # a child version and its original are one event: the pause covers both
                for n in np.nonzero(had_ev & HASFAM_[s_ev])[0]:
                    ev_last[n, ROOT == ROOT[s_ev[n]]] = t
            for n in np.nonzero(had_ev)[0]:
                lev_log.append((int(n), t, int(s_ev[n])))
            aff_d = aff * EVERYDAY[None]; near_e = None
            if BAT:   # a person whose rite of passage is late (a 20-year-old still juvenile) lives the everyday of their age:
                # when few ordinary moments are open in their stage and age (title and joining moments do not count, or
                # a choir member would meet the choir every week), the neighbouring stages' open moments join in. A
                # moment only resting (gap:) still counts as open; what joins keeps its own pause and the engine's reading
                rowz = ((aff_open * EVERYDAY[None] > 0) & REG_[None]).sum(1) < P["everyday_min"]
                if rowz.any():
                    near = L["STG"][:, np.minimum(stage[rowz] + 1, NS - 1)].T | L["STG"][:, np.maximum(stage[rowz] - 1, 0)].T
                    near &= ~L["STG"][:, stage[rowz]].T          # the stage's own moments are counted already
                    add_ = np.exp(2.0 * (nic[rowz] @ L["ALPHA"].T)) * (near & gate[rowz] & REG_[None]) * RATE[None] * cond_fac[rowz]
                    if WON:   # the world's gates hold here too: the spheres' (haunt, rung, sphere event) always, the rest
                        add_ = add_ * np.where(WL.new_gates[None] | P["near_gate"], mf_[rowz], 1.0)   # with near_gate
                    aff_d[rowz] += add_ * gapw_[rowz] if GAPXON_ else add_
                    near_e = np.zeros_like(aff_d); near_e[rowz] = add_   # open before their pauses (gap_keep)
            # never a life event as an ordinary week: if every everyday moment is resting, the least rested of the open
            # ones (their weight before the pause); only if none is open at all, anything open (Library 23:20)
            aff_e = aff_open * EVERYDAY[None]
            if BAT and P["gap_keep"] and GAPXON_:   # another moment's pause never raises a moment's own weekly chance: each
                # moment that is not ordinary routine (a door, a holder's moment, an inner one) keeps its share of everything
                # open before the pauses (its rate on the everyday scale); the ordinary routine fills the weeks the pauses free
                open_e = aff_e if near_e is None else aff_e + near_e
                tot_ = open_e.sum(1)
                reg_ = aff_d * ROUT_[None]; oth_ = (aff_d - reg_) / np.maximum(tot_, 1e-12)[:, None]
                oth_ = oth_ / np.maximum(oth_.sum(1, keepdims=True), 1.0)
                gx_ = np.ones(sit_last.shape, bool)   # speed pass: tested on the gapped moments' columns only
                gx_[:, GAPX_I] = (t - sit_last[:, GAPX_I]) / 52 >= GAPXLO_[:, GAPX_I]
                re_ = open_e * ROUT_[None] * gx_   # never inside its gap's lo
                rs_ = reg_.sum(1, keepdims=True); rse_ = re_.sum(1, keepdims=True)
                gf_ = P["gap_fill"]   # the freed weeks spread over the routine by its weight before (gf) and after its own pauses
                fw_ = gf_ * re_ / np.maximum(rse_, 1e-300) + (1 - gf_) * np.where(rs_ > 0, reg_ / np.maximum(rs_, 1e-300), re_ / np.maximum(rse_, 1e-300))
                fill_ = fw_ / np.maximum(fw_.sum(1, keepdims=True), 1e-300)
                kp_ = ((rs_ + rse_) > 0)[:, 0] & (tot_ > 0)
                aff_d[kp_] = oth_[kp_] + (1 - oth_[kp_].sum(1, keepdims=True)) * fill_[kp_]
            aff = np.where(aff_d.sum(1, keepdims=True) > 0, aff_d, np.where(aff_e.sum(1, keepdims=True) > 0, aff_e, aff))
        # a week with nothing open at all (once seen in the clan life, preset 5) has a zero row: no NaN weights, and the
        # pick is situation 0 as before (the NaN row's argmax); every other row divides as before, bit for bit
        aff /= np.maximum(aff.sum(1, keepdims=True), 1e-300)
        s = (aff.cumsum(1) > rng.random((N, 1))).argmax(1)
        if pausing:
            _pause_state(pz_st, ST_CELLS, ST_FR)
            s = yield Pause("situation", t, pz_st, s)
            pz_st._fr = None
            if NW_ON: nw_mark(NW_PLAYER)
        if P["base_rates"]:
            s = np.where(had_ev, s_ev, s)
        if BAT and P["base_rates"] and len(ECH):   # a due echo comes back in a week without a life event
            pe_ = (echo_ready & avail0[:, ECH_S] & ~once_done[:, ROOT[ECH_S]] & ~had_ev[:, None] & ~dead[:, None]) \
                * np.minimum(1, P["echo_w"] * echo_fac)                    # once: on an echo is honoured too
            fe_ = rng.random(pe_.shape) < pe_
            has_e = fe_.any(1)
            if has_e.any():
                e_pick = np.argmax(np.where(fe_, rng.random(fe_.shape), -1.0), 1)
                ie_ = np.nonzero(has_e)[0]
                s[ie_] = ECH_S[e_pick[ie_]]
                echo_anchor[ie_, e_pick[ie_]] = NEVER; echo_ready[ie_, e_pick[ie_]] = False
                if EP_ON:
                    ech_now[ie_] = e_pick[ie_]
        if EP_ON:
            s_ep = s.copy()   # a threshold season's step this week keeps its week (no return over it)
        sea_tr = np.zeros(N, bool)
        if SEA_AGE_ON:   # a stage's season not yet opened by its rite comes at its age (waiting for a running season to end)
            for k_ in SEA_KS:
                last_ = SEA_HI[k_] - SEA_LEN_Y
                due_ = ~sea_had[:, k_] & ~dead & (age >= sea_age[:, k_]) & (age <= last_ + 1 / 52) & ((sea_k < 0) | (age >= last_))
                if k_ == ELD_ and RET_SEA:   # later life opens with retiring; someone still at work by its last week opens it then
                    due_ &= (ret_pend < 0) & (~held[:, CAR] | (age >= last_))
                for n in np.nonzero(due_)[0]:
                    sea_open(n, k_)
        if SEA_ON and (sea_k >= 0).any():   # threshold season: the due step's moment in place of an ordinary week
            for n in np.nonzero(sea_k >= 0)[0]:
                dt_ = t - sea_t0[n]
                if dt_ > P["season_len"]:
                    sea_k[n] = -1; continue
                B[n] = max(B[n], P["season_open"])            # open through the season
                if had_ev[n] if P["base_rates"] else False:
                    continue                                   # a big life event this week: the step waits
                due_ = np.nonzero(~sea_done[n] & (dt_ >= SW_))[0]
                if not len(due_):
                    continue
                st_ = int(due_[np.argmin(SW_[due_])]); sea_done[n, :st_ + 1 if st_ < 3 else 0] = True; sea_done[n, st_] = True
                if st_ == 3:   # the transforming chance's own week: the season's transform: moment (any step)
                    c_ = np.nonzero((TH_K == sea_k[n]) & TH_TR & gate_sea[n])[0]
                else:          # a step: its plain moments first; its transform: moment only when no plain one is open
                    c_ = np.nonzero((TH_K == sea_k[n]) & (TH_STEP == st_ + 1) & gate_sea[n])[0]
                    if (~TH_TR[c_]).any():
                        c_ = c_[~TH_TR[c_]]
                    elif len(c_):
                        sea_done[n, 3] = True
                if ret_pend[n] >= 0 and st_ == 0:             # retiring: the season opens on the last day at work
                    cr_ = c_[RETIRES_[c_]]
                    if len(cr_):
                        c_ = cr_
                    elif held[n, CAR]:
                        end([n], [CAR], "retired", t); ret_pend[n] = -1
                if len(c_) and P["season_excl"]:    # K6: one draw for the step; each moment at its own share, tilted by
                    tl_ = np.exp(2.0 * (nic[n] @ L["ALPHA"][c_].T))   # the person's colours (share-weighted mean tilt 1)
                    pp_ = TH_P[c_] * tl_ * TH_P[c_].sum() / max((TH_P[c_] * tl_).sum(), 1e-12)
                    pp_ = pp_ / max(1.0, pp_.sum()); k_ = int(np.searchsorted(np.cumsum(pp_), sea_rng.random(), side="right"))
                    c_ = c_[k_:k_ + 1]                # past the sum: the step passes as an ordinary week
                elif len(c_) and P["season_share"]:   # each step moment comes to its share of lives (Library next3 §4): a
                    c_ = c_[sea_rng.random(len(c_)) < TH_P[c_]]   # step none of whose moments comes passes as an ordinary week
                if len(c_):
                    wt_ = np.exp(2.0 * (nic[n] @ L["ALPHA"][c_].T)) * RATE[c_]
                    s[n] = c_[rng.choice(len(c_), p=wt_ / wt_.sum())]
                    sea_tr[n] = TH_TR[s[n]]
                if sea_done[n].all():
                    sea_k[n] = -1
        if EP_ON:   # picks come back: a due seed's return, or an ordinary echo of its kind told as its return
            ep_return(s, s_ep)
            ech_now[:] = -1
        # a commitment that no longer fits what the person wants, and keeps disappointing, comes up for reconsideration
        a_now = softmax(y)
        misfit = _uclip(1 - 5 * (prof * a_now[:, None, :]).sum(-1), 0, 1)   # wanting what it stands for less than an even share
        p_re = held * P["recon_p"] * (1 - sat) * (1 + 3 * misfit) * (stage >= 2)[:, None]   # children cannot walk away
        mf_ = np.where(held, misfit, -1.0) if P["recon_held"] else misfit   # (the game's family check: a partner left twice)
        p_re = np.where(force_re[:, None] & (mf_ > P["clash_off"]) & (mf_ >= mf_.max(1, keepdims=True)), 1.0, p_re)
        force_re[:] = False
        hit = rng.random((N, NK)) < p_re
        rk = np.where(hit.any(1), np.argmax(np.where(hit, p_re, -1.0), 1), -1)
        recon = rk >= 0
        s = np.where(recon, L["RECON"], s)
        if EP_ON and (recon & (ep_now >= 0)).any():   # reconsidering takes the week: the seed waits for another
            for n in np.nonzero(recon & (ep_now >= 0))[0]:
                sd_ = ep_seeds[ep_now[n]]; sd_["done"] = sd_["got"] = None; ep_now[n] = -1
        sit_n[np.arange(N), s] += 1                              # how often each situation came up in each life
        if SK_ON:   # v25 seek: what they met lately (diminishing returns, curiosity)
            RX.encounter(L["ALPHA"][s], ~dead)
        m = L["M"][s]; e = Eeff[s]; e0 = L["E"][s]; diff = L["DIFF"][s]; mask = L["MASK"][s]
        stakes = L["STAKES"][s]; alpha = L["ALPHA"][s]; oid = L["OID"][s]
        ri = np.nonzero(recon)[0]; rkk = rk[ri]
        if len(ri):
            pk = prof[ri, rkk]
            m[ri, 0] = pk; m[ri, 1] = 0.5 * pk + 0.5 * a_now[ri]; m[ri, 2] = EXIT
            e[ri, :3] = 0.7 * m[ri, :3]
        do_nothing = (m.std(-1) < 1e-9)
        closed_s = L["CLOSED"][s] if BAT else None
        pbump = 0.0; earn = 0.0; lackf = 1.0
        if RON:   # an act that needs a title or perk the person lacks: impossible (acting as what one is not), or closed by
            rq_ = GR["A_REQ"][s]                                  # law, approval or means (the act's without:, else the kind's)
            unmet = (rq_ >= 0) & ~r_has[ar[:, None], np.maximum(rq_, 0)]
            if unmet.any():
                wk_ = np.where(GR["A_WITHOUT"][s] >= 0, GR["A_WITHOUT"][s], GR["without_default"][np.maximum(rq_, 0)])
                mask = mask & ~(unmet & (wk_ == 3))
                closed_s = np.where(unmet & (wk_ < 3) & (closed_s < 0), wk_, closed_s)
                if LACK_ON:
                    lackf = np.where(unmet, A_LACK[s], 1.0)
            # skills and standing make acts in their ways likelier to work (a lapsed skill counts at its fading level)
            hp_ = r_has[:, NT_:]                                 # the best perk in each color counts fully, the rest a little
            cb_ = (np.where(MEM_K, np.maximum(hp_, p_lev), hp_) * ODD4)[:, :, None] * INDP[None]      # N,perks,C (logit units)
            mx_ = cb_.max(1); PB = np.minimum(mx_ + P["perk_breadth"] * (cb_.sum(1) - mx_), P["perk_cap"])
            pbump = np.einsum("nkc,nc->nk", m, PB)
            gr_ = A_GR1[s]; gi_ = np.maximum(gr_, 0)             # regaining a lapsed licence or skill is easier while it lasts
            pbump = pbump + np.where((gr_ >= 0) & ~r_has[ar[:, None], gi_], p_lev[ar[:, None], np.maximum(gi_ - NT_, 0)], 0.0)
            at_ = missed_at(GR["A_EARN"][s], s) if EARN_ON else None   # N,K: the title (else perk) each option's act earns for
            if AMS_ON:   # {missed}: the budget's cut on the title missed (the written chance carries it for the others)
                pbump = pbump + np.where(AMS_[s] & (missed_t[:, None] >= 0), TZM_[np.maximum(missed_t, 0)][:, None], 0.0)
            if EARN_ON and (at_ >= 0).any():   # prepared for the title the act gives (HELPS), and the right time (WINDOWS)
                rw_ = np.nonzero((at_ >= 0).any(1))[0]; ai_ = np.maximum(at_[rw_], 0)
                hw_ = r_has[rw_].astype(np.float32)
                if P["rung_years"] > 0:   # a rung counts by the years on it (Emren 09:18; packs 09:21)
                    yk_ = black_k()[rw_, None] if RP_ON and P["black_edge"] else 1.0   # black_edge: Black climbs faster
                    hw_[:, :NT_] *= np.minimum(np.maximum(t - r_since[rw_, :NT_], 0) * yk_ / (52.0 * P["rung_years"]), 1.0)
                prep_ = (np.einsum("ni,nki->nk", hw_, GR["HELP"][ai_])
                         + np.einsum("nm,nkm->nk", (mark_n[rw_] > 0).astype(np.float32), GR["HELP_MK"][ai_][:, :, :NM])) \
                    / np.maximum(GR["HELP_N"][ai_], 1)
                er_ = P["help_lift"] * np.minimum(prep_, 1.0) \
                    + P["try_lift"] * np.minimum(tries_ct[rw_[:, None], ai_], P["try_max"])   # earlier tries at it
                if P["base_rates"]:   # the context that opens this moment's window (driver words), good times or bad
                    wr_ = L["WINDOW_REF"][s[rw_]]
                    er_ = er_ + P["window_lift"] * _uclip((X[rw_] * L["WINDOW"][s[rw_]]).sum(1) / np.maximum(wr_, 1e-9), -1, 1)[:, None]
                earn = np.zeros((N, L["K"])); earn[rw_] = er_ * (at_[rw_] >= 0) * GR["LIFT"][ai_]
        if AQ_ON:   # v7: an act that needs a state the person is not in (wealthy, fit): not offered, or closed by means
            aq_ = L["ADJ_REQ"][s]
            un_ = (aq_ >= 0) & ~adj[ar[:, None], np.maximum(aq_, 0)]
            if un_.any():
                wk_ = np.where(L["ADJ_WOUT"][s] >= 0, L["ADJ_WOUT"][s], ADJ_WITHOUT[np.maximum(aq_, 0)])
                mask = mask & ~(un_ & (wk_ == 3))
                closed_s = np.where(un_ & (wk_ < 3) & (closed_s < 0), wk_, closed_s)
                if LACK_ON:
                    lackf = lackf * np.where(un_, A_LACK[s], 1.0)
        if BAT and CLU_ON:
            clu_ = (closed_s >= 0).astype(float)
        if BAT and IDC_ON:   # N1b: crossing the role the world expects, or naming one's own gender, is closed by approval as
            # strongly as the world frowns on it (in units of a written closed: approval; where one is written, the larger)
            rs_w, at_w, ex_w = role_view()
            ra_ = ROLE_ACT[s]; rc_ = _uclip(ra_, 0, 1)
            cw_ = np.where(ra_ == 3, 1.0, np.where(ra_ < 2, np.take_along_axis(ex_w, 1 - rc_, 1), 0.0)) * (ra_ >= 0)
            u_ = P["role_k"] * rs_w[:, None] * cw_ * np.where(~female & (age < 13), P["role_boys"], 1.0)[:, None]
            u_ = np.maximum(u_, (TRANS_OPT[s] | (OPENMK_[s] & named_g[:, None])) * 2.0 * (1 - at_w)[:, None])
            clu_ = np.where(closed_s >= 0, np.maximum(1.0, u_), u_)
            closed_s = np.where((closed_s < 0) & (u_ > 0), 1, closed_s)
        if BAT and WON:   # the world's law, norms and technology (world-fields.md): a written closed: law opens where the law
            # allows it; an option with law: is closed by the law where it is (banned 1 unit, restricted half); norm: costs
            # 2 x (1 - acceptance) units of approval; tech: is not offered without the technology, and closed by means as
            # far as the person's class lacks it
            ul_, lo_, ua_, um_, gone_ = WL.closures(s, partner_same if ID2 else np.zeros(N, bool), age)
            if WFX_ON:
                wco_.update(s=s.copy(), ul=ul_, lo=lo_, ua=ua_, um=um_, gone=gone_, closed0=closed_s.copy(),
                            role=u_.copy() if IDC_ON else None)
            op_ = lo_ & (closed_s == 0)
            clu_ = np.where(op_, 0.0, clu_); closed_s = np.where(op_, -1, closed_s)
            for kd_, u2_ in ((0, ul_), (1, ua_), (2, um_)):
                closed_s = np.where((closed_s < 0) & (u2_ > 0), kd_, closed_s)
                clu_ = np.maximum(clu_, u2_)
            mask = mask & ~gone_
            if CL_ON:   # v25 clash: a clash moment's infeasible families are not offered (no exit, nobody to talk to)
                mask = RX.clash_mask(s, mask)
            diff = diff + WL.odds(s)   # finding work by local unemployment, education by places, treatment by hospitals
            if SV_ON:   # phase 5, service as a chapter: 5 years after the guard or the host, hiring is easier in prot and
                # rule work and a little harder elsewhere; 10 years after prison, harder by the record's weight (Pager 2003)
                jo_ = WL.job_o[s]
                if jo_.any():
                    se_ = r_end[:, SVC_T].max(1) if len(SVC_T) else np.full(N, NEVER)
                    vet_ = (se_ > NEVER) & (t - se_ < 52 * SVS_["after_guard_or_host"]["years"])
                    if len(SVC_T):
                        vet_ &= ~r_has[:, SVC_T].any(1)
                    rec_ = (pris_out > NEVER) & (pris_out <= t) & (t - pris_out < 52 * SVS_["after_prison"]["years"])
                    pr_ = PR_T[np.where(GR["A_TITLE"][s] >= 0, GR["A_TITLE"][s], NT_)]
                    diff = diff + jo_ * (vet_[:, None] * np.where(pr_, SV_D[0], SV_D[1]) + rec_[:, None] * SV_D[2])
                    br_ = (brec > NEVER) & (t - brec < 7 * YR_)   # a bank's record: hiring a little harder
                    diff = diff + jo_ * (br_[:, None] * DB_D)
            if PT_ON and pt_act.any():   # part 4: a job lead through a former inmate: hiring x 1.1 in farm and industry work
                diff = diff + (WL.job_o[s] & PT_SEC[np.where(GR["A_TITLE"][s] >= 0, GR["A_TITLE"][s], NT_)]) * (pt_act[:, None] * PT_D)
        if BAT and CLU_ON:
            diff = diff + P["closed_diff"] * clu_
        elif BAT:   # closed by law, approval or means: still pickable, but harder
            diff = diff + P["closed_diff"] * (closed_s >= 0)

        if t == 6 * 52:                                      # raised in a faith: the family's, not a choice
            shu_ = rng.random(N); inh = shu_ < P["faith_inherit"]
            if STH_ON:   # v22.5, F12: raised in the family's own faith (the world's), in none when the family holds none;
                # a start that promises a faith or none keeps it (faith_inherit 1 or 0; the birth was drawn to fit)
                shfi_ = P["faith_inherit"]; shpf_ = np.asarray(WL.PP.pfaith, np.int64)
                inh = np.full(N, shfi_ >= 1) if (shfi_ <= 0 or shfi_ >= 1) else (shpf_ >= 0) & (shu_ < P["faith_fam_p"])
            held[inh, FAI] = True; I[inh, FAI] = 0.3; since[inh, FAI] = t; sat[inh, FAI] = 0.7; faith_given[inh] = True
            prof[inh, FAI] = rng.dirichlet(np.full(C, P["faith_conc"]), inh.sum())     # families hold many kinds of faith
            if STH_ON and inh.any():   # the family's faith's own ways
                shfp_ = np.asarray(WL.W.faith_profile, float); shfp_ = shfp_ / shfp_.sum(1, keepdims=True)
                shk_ = inh & (shpf_ >= 0)
                prof[shk_, FAI] = shfp_[np.minimum(shpf_[shk_], len(shfp_) - 1)]
            for n in np.nonzero(inh)[0]:
                commit_log.append((int(n), t, FAI, "inherited", prof[n, FAI].round(2).tolist(), 0.3))
                if n in events:
                    events[n].append(dict(commitment=dict(age=6.0, kind="faith", what="inherited", profile=prof[n, FAI].round(2).tolist())))

        # ---- v7: how far each option of this week's situation serves each goal (fit with its ways, or a step into its domain)
        if GON:
            cf = _uclip((5 * np.einsum("nkc,ngc->ngk", m, gm) - 1) / 2, 0, 1)
            dstep = (gd[:, :, None] >= 0) & (L["COMMIT"][s][:, None, :] == gd[:, :, None])
            rel = np.where(((gk == 2) & (gd >= 0))[:, :, None], np.maximum(dstep * (0.5 + 0.5 * cf), 0.5 * cf), cf)
            rel = rel * (mask & ~do_nothing)[:, None, :] * (gk >= 0)[:, :, None]
            wR = gs * np.select([gk == 0, gk == 1, gk == 2], [P["g_dream"], P["g_pass"], P["g_plan"]], 0.0)
            wI = gs * np.select([gk == 1, gk == 2], [P["g_pass_auto"] * (1.5 - ga), P["g_plan_auto"]], 0.0)
            gU_R = np.einsum("ng,ngk->nk", wR, rel); gU_I = np.einsum("ng,ngk->nk", wI, rel)
            gN = P["g_notice"] * np.einsum("ng,ngk->nk", gs * (gk >= 0), rel)
            # what a person's weeks usually offer: ways strongly in each color, steps into each domain (for felt odds)
            rk_ = mask & ~do_nothing
            pres_c = pres_c * (1 - 1 / 104) + (np.where(rk_[..., None], m, 0).max(1) >= 0.5) / 104
            pres_d = pres_d * (1 - 1 / 104) + HAS_STEP[s] / 104
            pres_n = pres_n * (1 - 1 / 104) + 1 / 104
        else:
            gU_R = gU_I = gN = 0.0

