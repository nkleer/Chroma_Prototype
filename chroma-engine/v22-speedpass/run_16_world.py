# run_16_world.py: part 16 of 18 of engine._run, the life loop.
# 4b. the outside world: eras, personal events, needs from resources, aspiration, pressure.
# Lines here are _run's own, unchanged and at their own indent: engine.py joins the parts in order (engine.RUN_PARTS)
# and compiles them as one, so a name used here may be set in an earlier part. Never import or run it alone.
        # ---- 4b. the outside world. An era begins: everyone gets its message at once
        if RX_ON and t % 4 == 0:   # v25 react: a disaster in their town this month (before the outside events read it)
            rx_dis = np.asarray(WL.dis_own, float).copy()
        if t in era_at:
            key, inten, kind = era_at[t]
            msg = np.tile(COMBO_MIX[key], (N, 1)); ex = era_expo(ERA_KINDS.index(kind)); ac = accept(ar, msg, 1.0)
            if WON:   # close first (Emren 10:39; spec 1 §4): with the world on the era reaches a life mostly through its people
                # (their niche carries the times), so its own message is half as strong, and weighs most at 15 to 25
                ex = ex * 0.5 * float(np.interp(age, [10, 15, 25, 40], [0.3, 1.0, 1.0, 0.5]))
            take_in(ar, msg, P["era_shock"] * inten * ex * ac, 8)
            stress += 0.2 * inten
            for n in events:
                events[n].append(dict(era=dict(age=round(age, 2), combo=key, name=IDEAS[key][0], idea=IDEAS[key][1], kind=kind,
                                               intensity=round(inten, 2), took=round(float(ac[n]), 2))))
        # personal events: peers, institutions, daily life, nature, the supernatural
        if P["events_on"]:
            rates = EV["rate"] * P["ev_scale"] * EV_KEEP; tot = rates.sum()
            ii = np.nonzero(rng.random(N) < tot)[0]
            if len(ii):
                j = rng.choice(len(rates), size=len(ii), p=rates / tot); kind = EV["kind"][j]
                msg = np.zeros((len(ii), C))
                sel = kind == "fixed"; msg[sel] = EV["mix"][j[sel]]
                sel = kind == "random"; msg[sel] = random_messages(rng, int(sel.sum()))
                sel = kind == "niche"; msg[sel] = nic[ii[sel]] / nic[ii[sel]].sum(1, keepdims=True)
                sel = kind == "faith"; mf = random_messages(rng, int(sel.sum())); hf = held[ii[sel], FAI]
                mf[hf] = prof[ii[sel][hf], FAI]; msg[sel] = mf
                src = EV["src"][j]
                expo = np.select([src == 0, src == 1, src == 2, src == 3, src == 4],
                                 [0.5 + res[ii, TIE] + 0.5 * held[ii, COM] * I[ii, COM], inst_expo()[ii], np.ones(len(ii)),
                                  0.5 + (1 - res[ii, MON]), 0.4 + held[ii, FAI] * (0.6 + I[ii, FAI])])
                ac = np.zeros(len(ii)); hm = kind != "none"
                if hm.any():
                    ac[hm] = accept(ii[hm], msg[hm], (src[hm] <= 1).astype(float))
                    take_in(ii[hm], msg[hm], EV["s"][j[hm]] * expo[hm] * ac[hm], 7)
                need[ii] += EV["need"][j]; res[ii] = _uclip(res[ii] + EV["res"][j], 0, 1)
                if NW_ON: nw_mark(NW_OUT)
                stress[ii] += 0.3 * EV["s"][j] * (EV["need"][j].sum(1) < 0)
                mv = EV["move"][j]; nic[ii[mv]] = 0.5 * nic[ii[mv]] + 0.5 * msg[mv]; res[ii[mv], TIE] = np.maximum(0, res[ii[mv], TIE] - 0.2)
                dr = EV["door"][j]; nic[ii[dr]] += 0.15 * EV["s"][j[dr], None] * (msg[dr] - nic[ii[dr]])
                for q_, n in enumerate(ii):
                    ev_log.append((int(n), t, int(j[q_]), float(ac[q_])))
                    if n in events:
                        events[n].append(dict(outside=dict(age=round(age, 2), name=EV["names"][j[q_]], source=SOURCES[src[q_]],
                                                           message=msg[q_].round(2).tolist() if hm[q_] else None,
                                                           took=round(float(ac[q_]), 2) if hm[q_] else None)))
        if BAT and len(EVR) and t % 4 == 0:   # outside events from the batch, each read through the person's own colors
            dis_src_ = {}   # life -> (hazard, "home" or "near"): the world's disaster that brings its outside event (WL6)
            if WON and DIS_J_:   # a disaster's outside event comes when the world's disaster strikes one's own town or a
                # close person's (spec 5 §2: the history dial reaches the life through it), not on its own clock
                own_, near_ = WL.disasters()
                hit_ = ((own_ > 0) & (rng.random(N) < 0.4 + 0.5 * own_)) | (near_ & (rng.random(N) < WLM.DIS_NEAR))
                for j_ in DIS_J_:
                    evr_next[:, j_] = np.where(hit_ & (t >= evr_ok[:, j_]), t, T + 1)
                if events or WFX_ON:   # the story names the hazard that struck (WL6), so its scene can fit it
                    dis_src_ = {int(n): ((WL.dis_haz_now[n], "home") if own_[n] > 0 else (WL.dis_nhaz_now[n], "near"))
                                for n in np.nonzero(hit_)[0] if n in events or WFX_ON}
                if P["dis_match"]:   # WL6: only the events of the hazard that struck their own town
                    for n in np.nonzero(hit_ & (own_ > 0))[0]:
                        ok_ = DIS_FOR_.get(WL.dis_haz_now[n], DIS_J_)
                        for j_ in DIS_J_:
                            if j_ not in ok_:
                                evr_next[n, j_] = T + 1
                if WFX_ON:
                    for n in np.nonzero(((own_ > 0) | near_) & ~dead)[0]:
                        rc_ = WL.dis_rec_now[n] if own_[n] > 0 else None
                        wfx_add(n, "disaster", "home" if own_[n] > 0 else "close person", own_[n] if own_[n] > 0 else 1.0, age,
                                cause=None if rc_ is None else dict(domain=rc_.get("domain"), kind=rc_.get("kind"),
                                                                    key=rc_.get("key"), age=round(age, 2)),
                                hazard=WL.dis_haz_now[n] if own_[n] > 0 else None)
            due_ = evr_next <= t
            if due_.any():
                ns = cond_ns(t, age, w)
                lens_ = 0.5 * softmax(k) + 0.5 * w
                for j_ in np.nonzero(due_.any(0))[0]:
                    e_ = EVR[j_]; ii_ = np.nonzero(due_[:, j_])[0]
                    evr_next[ii_, j_] = t + rng.uniform(e_["gap"][0], e_["gap"][1], len(ii_)) * 52
                    if not (e_["window"][0] <= age <= e_["window"][1]):
                        continue
                    p_ = _uclip(P["read_p"] * factor(e_, ns)[ii_], 0, 1) * ev_cond(e_["req"], ns)[ii_]
                    ii_ = ii_[rng.random(len(ii_)) < p_]
                    if not len(ii_):
                        continue
                    if WON:
                        evr_ok[ii_, j_] = t + e_["gap"][0] * 52
                    pr_ = softmax(P["read_beta"] * 5 * lens_[ii_] @ e_["lens"].T)
                    rd_ = (pr_.cumsum(1) > rng.random((len(ii_), 1))).argmax(1)
                    imp_ = e_["impact"][rd_]
                    an_ = np.array([e_["also"][r_][0] for r_ in rd_]); ar_ = np.array([e_["also"][r_][1] for r_ in rd_])
                    thr_ = np.maximum(-np.asarray(e_["base_need"], float), 0)   # P4 §4: the needs it threatens
                    ev_by_ = (P["ev_need_k"] or P["ev_state_k"] or P["ev_reach_k"]) and thr_.sum() > 0
                    if ev_by_:
                        thr_ = thr_ / thr_.sum()
                        calm_ = _uclip(peace[ii_] + content[ii_] - 0.5, 0, 1)   # at peace and content: 1; strained: 0
                        if P["ev_need_k"]:   # it lands harder on a need already lacking
                            imp_ = imp_ * _uclip(1 + P["ev_need_k"] * (lack[ii_] @ thr_ - 0.3), 0.5, 2.0)
                    need[ii_] += P["read_k"] * imp_[:, None] * e_["base_need"][None] + an_
                    if NW_ON: nw_mark(NW_READ)
                    r0_ = res[ii_].copy() if WFX_ON and j_ in DIS_J_ else None
                    res[ii_] = _uclip(res[ii_] + imp_[:, None] * e_["base_res"][None] + ar_, 0, 1)
                    if r0_ is not None:   # what a disaster cost them: money, time, health, ties, freedom
                        for q_, n in enumerate(ii_):
                            for ri_ in np.nonzero(np.abs(res[n] - r0_[q_]) >= P["wfx_step"])[0]:
                                wfx_add(n, "disaster", RESOURCES[ri_], res[n, ri_] - r0_[q_, ri_], age, moment=e_["name"],
                                        hazard=dis_src_.get(int(n), (None, None))[0])
                    good_ = e_["base_need"].sum() + e_["base_res"].sum() >= 0
                    if good_:
                        mood[ii_] += 0.1 * imp_
                    else:
                        stress[ii_] += 0.3 * imp_ * ((1 + P["ev_state_k"] * (1 - 2 * calm_)) if ev_by_ and P["ev_state_k"] else 1.0)
                        mood[ii_] -= 0.1 * imp_
                    msg_ = np.eye(C)[e_["want"][rd_]]
                    take_in(ii_, msg_, P["read_want"] * imp_, 7)
                    if ev_by_ and P["ev_reach_k"] and not good_:   # they reach for what their own table ties to safety
                        tb_ = NMP[ii_] if NM_ON else np.repeat(NMAP[None], len(ii_), 0)   # (strained) or belonging (calm)
                        rch_ = (1 - calm_)[:, None] * tb_[:, NIDX["safety"]] + calm_[:, None] * tb_[:, NIDX["belonging"]]
                        take_in(ii_, rch_ / np.maximum(rch_.sum(1, keepdims=True), 1e-9), P["ev_reach_k"] * imp_, 7)
                    for q_, n in enumerate(ii_):
                        read_log.append((int(n), t, int(j_), int(rd_[q_])))
                        if n in events:
                            rdd_ = dict(age=round(age, 2), name=e_["name"], reading=e_["labels"][rd_[q_]],
                                        say=e_["say"][rd_[q_]], impact=float(imp_[q_]))
                            if int(n) in dis_src_ and WON and j_ in DIS_J_:   # WL6: the hazard that struck, and where
                                rdd_.update(hazard=dis_src_[int(n)][0], where=dis_src_[int(n)][1])
                            events[n].append(dict(read=rdd_))
        # resources and commitments feed needs: safety (money, health), belonging (ties), autonomy (freedom, time)
        supply = np.stack([0.5 * res[:, MON] + 0.5 * res[:, HEA], res[:, TIE], 0.6 * res[:, FRE] + 0.4 * res[:, TIM]], 1)
        if WON:   # the world: safety from crime, war and disaster where one lives; belonging from one's settings and people
            supply[:, 0] += WL.safety(); supply[:, 1] += 0.5 * (np.asarray(WL.PP.belong, float) - WLM.BELONG_REF)
            if WFX_ON:   # what the place gives to feeling safe, by the world's cause
                wfx_track("safety", WL.safety_parts(), age, dead)
        need[:, :3] += P["res_need"] * (supply - 0.5)
        if NW_ON: nw_mark(NW_MEANS)
        need += P["commit_need"] * ((held * I) @ KPAY) * ((1 - need) if P["satiate"] else 1)
        if NW_ON: nw_mark(NW_COMMIT)
        if MK_ON:   # the mark of the work: a trade with say and skill meets autonomy and competence more (Jahoda 1982)
            mz_ = np.asarray(WL.PP.mark_z, float) * (held[:, CAR] * I[:, CAR])[:, None]
            need[:, NIDX["autonomy"]] += 0.1 * P["commit_need"] * mz_[:, 0]; need[:, NIDX["competence"]] += 0.1 * P["commit_need"] * mz_[:, 1]
            if NW_ON: nw_mark(NW_COMMIT)
        if RON:   # a title's own needs on top of its kind's, scaled the same way (statuses at full strength)
            tn_ = (r_has[:, :NT_] * np.where(TK_ < NK, I[:, np.minimum(TK_, NK - 1)], 1.0)) @ GR["meets_need"]
            need += P["commit_need"] * P["title_need"] * tn_ * np.where(tn_ > 0, (1 - need) if P["satiate"] else 1, 1)
            if NW_ON: nw_mark(NW_TITLE)
        stress += 0.01 * np.maximum(0, 0.5 - res[:, HEA])
        if DEEP_ON and getattr(WL.PP, "care_load", None) is not None:   # phase 5: the care load wears on the carer
            stress += P["care_stress"] / 4.33 * np.asarray(WL.PP.care_load, float) / 10
        # a family looks after its children: safety and belonging are mostly provided before adolescence
        care = P["family_care"] * np.where(stage == 0, 1.0, np.where(stage == 1, 0.5, 0.0))
        need[:, :2] += care[:, None] * (0.85 - need[:, :2])
        need[:, 3:] += 0.5 * care[:, None] * (0.7 - need[:, 3:])     # and school and play give some competence and meaning (v5)
        if NW_ON: nw_mark(NW_CARE)
        need = _uclip(need, 0, 1)
        if NW_ON: nw_clip()
        lack_raw = np.maximum(0, P["need_set"] - need) / P["need_set"]
        if P["flex"]:      # v6: needs that stay unmet lose importance, slowly, and faster with age; met ones regain it
            # driven by experience, not age (Emren 2026-10-04: favor comes from preference, mindset and experience):
            # the more wanted things a person has seen fail or close, the more readily they let go of what stays unmet
            fa = _uclip((tries - wins + blocked - P["flex_exp"][0]) / P["flex_exp"][1], 0, 1)[:, None]
            nimp += P["flex_rate"] * fa * ((1 - P["flex_depth"] * lack_raw) - nimp) + P["flex_rate"] * 0.2 * (1 - nimp)
        lack = nimp * lack_raw + P["duty_w"] * P["duty_asp"] * np.minimum(1, (held * I) @ DUTY)
        felt = np.einsum("nj,njc->nc", lack, NMP) if NM_ON else lack @ NMAP   # how much each color's ends could meet what is lacking
        dV = P["zeta"] * (w / w.max(1, keepdims=True)) * felt * (SE - P["eps0"])   # v2 direct channel (zeta=0 in v3)
        stress += 0.02 * (nimp * lack_raw).sum(1)

        conf = P["chi"] * (w[:, 0] + w[:, 4] - w[:, 3] - w[:, 2])
        if RX_ON and (t % 4 == 0 or (SCN_ON and any(scn_demand))):   # v25 react (world_react.py): this month's demands and
            # responses (and the caller's this week); each demand's source's part of the pull is the demand's this month
            nimp_s_ = np.maximum(nimp.sum(1), 1e-9); rxc_ = WL.PP
            _cw_ = rxc_._rx_close[2] if getattr(rxc_, "_rx_close", None) is not None else np.zeros(N)
            _cs_ = rxc_._rx_close[1] if getattr(rxc_, "_rx_close", None) is not None else np.zeros((N, C))
            _cwk_ = float(rxc_.P.get("close_w", 0.15) or 0.15)
            _tot_ = np.asarray(rxc_._setw, float) + _cwk_ * _cw_
            _msc_ = np.where(_tot_[:, None] > 1e-9, (np.asarray(rxc_._setmix, float) + _cwk_ * _cs_) / np.maximum(_tot_, 1e-9)[:, None], w)
            _b0_, _pk_, _at_, _wd_ = rxc_.P["times_w"]; _tw_ = _b0_ + _pk_ * np.exp(-((age - _at_) / _wd_) ** 2)
            _cb_, _cp_, _ca_, _cwd_ = P["cur_age"]; _ce_ = _cb_ + _cp_ * np.exp(-((age - _ca_) / _cwd_) ** 2)
            _ck_ = (P["cur_rel_k"] if P["cur_rel"] else 5 * P["cur_k"]) * _ce_ * P["era_push_k"] if CUR_ON else 0.0
            _cm_ = np.asarray(P["cur_mix"], float) / sum(P["cur_mix"])
            _soc_k_ = (conf + P["social_child"] * np.where(stage == 0, 1.0, np.where(stage == 1, 0.5, 0.0))) * (1 - SOC_OWN)
            _af_, _as_ = ((AIM["face"][np.maximum(ak, 0)], astr * (ak >= 0)) if AIM_ON else (gm, gs * (gk >= 0)))
            _ind_ = RX._ind(age, held[:, CAR].astype(float), res[:, MON], res[:, FRE])
            rx_ctx = dict(w=w, conv=0.5 * w + 0.5 * softmax(k), plast=plast, dead=dead, loc=np.asarray(rxc_.loc), need=need,
                          lack=lack, lack_all=lack, nimp=nimp, res=res, held=held, I=I, prof=prof, aim_face=_af_, aim_s=_as_,
                          kidx={"work": CAR, "congregation": FAI, "partner": PAR}, cares=(held[:, PAR] | held[:, KID]).astype(float),
                          res_tim=res[:, TIM], res_mon=res[:, MON], need_aut=need[:, NIDX["autonomy"]],
                          nimp_aut=nimp[:, NIDX["autonomy"]] / nimp_s_ * len(NEEDS) / 5, means_low=np.clip(2 * (0.5 - res[:, MON]), 0, 1),
                          ind=_ind_, held_car=held[:, CAR].astype(float), faith_i=held[:, FAI] * I[:, FAI],
                          farm=(np.asarray(rxc_.psector) == WLM.WK.SECTORS.index("farm")).astype(float),
                          par_yrs=np.where(held[:, PAR], (t - since[:, PAR]) / 52, 0.0), btrust=btrust if BT_ON else None,
                          dis_own=None if rx_dis is None else np.where(rx_dis != RX.__dict__.get("_dis_last", 0), rx_dis, 0.0),
                          nmp=NMP, tot_nic=_tot_, msc=_msc_, tw=_tw_, a_nic=0.8 * plast * _soc_k_, a_cl=plast * _ck_ * _cm_[0],
                          a_pl=plast * _ck_ * _cm_[1], tot_cl=_cw_, nic=nic, belong=np.asarray(rxc_.belong, float),
                          f_need=(nimp * need).sum(1) / nimp_s_, content=content, stress=stress,
                          lack_comp=lack[:, NIDX["competence"]], lack_mean=lack[:, NIDX["meaning"]],
                          cur=cur_m, cur_rel=bool(P["cur_rel"]))
            if rx_dis is not None:
                RX._dis_last = rx_dis; rx_dis = None
            RX.month(t, age, rx_ctx, scn_only=t % 4 != 0)
            if t % 4 == 0:   # the states, the year's involvement, seeking
                rx_ctx.update(aim_block=RX.aim_block(t, astr if AIM_ON else None, astep if AIM_ON else None),
                              engage=RX.engage(tries))
                ds_, dm_ = RX.states_month(t, rx_ctx)
                stress = stress + ds_; mood = mood + dm_
                states = RX.states_view()
                if t % 52 == 0:
                    RX.involve_year(rx_ctx)
                if CL_ON:
                    RX.clash_now_update()
                if SK_ON:
                    RX.seek_month(t, age, rx_ctx); seek = RX.seek_view()
        obs = softmax(3 * f_tot)
        soc_ = nic if not SOC_OWN else (1 - SOC_OWN) * nic + SOC_OWN * onic   # soc_own: and the company they pick
        if RX_ON:   # v25 react: the sources whose demand came this month pull through it, not through the niche
            soc_ = soc_ + (1 - SOC_OWN) * RX.dnic
        dS = conf[:, None] * (soc_ - w) + P["xi"] * (obs - w)
        if P["social_child"]:   # v6: children take on the ways of the family around them, whatever their own lean
            dS += P["social_child"] * np.where(stage == 0, 1.0, np.where(stage == 1, 0.5, 0.0))[:, None] * (soc_ - w)
        if P["react_k"]:   # v6 (Library notes A6; Brehm): strong pressure on a steady person pushes them the other way
            s_n = np.tanh(steady / P["steady_cap"])
            press = 0.5 * np.abs(soc_ - w).sum(1)
            rs = _uclip((s_n - 0.5) / 0.5, 0, 1) * _uclip((press - P["react_press"]) / P["react_press"], 0, 1)
            dS -= P["react_k"] * P["chi"] * rs[:, None] * (soc_ - w)

        # aspiration: what the person wants to be. Needs, norms and role models act here
        a_ = softmax(y)
        conf_a = P["chi_a"] / P["chi"] * conf if P["chi"] else 0 * conf
        aligned = _uclip(5 * (ma * (a_ - w)).sum(1), 0, 1) * (~idle)       # how far this act was a step toward the want
        # the times: an era's norms, taken or pushed back according to the person (exposure x acceptance)
        times = np.zeros((N, C))
        if e_i > 0:
            ep = np.tile(e_p, (N, 1)); times = P["era_norm"] * e_i * (era_expo(era_k[t]) * accept(ar, ep, 1.0))[:, None] * (ep - a_)
        # feedback from the meta variables: discontent wants what is missing (unmet needs) and what seems to work
        # for others; contentment settles the want on who one is; restlessness wants out of inner color tension
        fs = felt.sum(1, keepdims=True); felt_n = np.where(fs > 1e-9, felt / np.maximum(fs, 1e-9), obs)
        disc = np.maximum(0, 0.5 - content)[:, None] * (0.5 * felt_n + 0.5 * obs - a_)
        settle_ = np.maximum(0, content - 0.6)[:, None] * (w - a_)
        tgrad = np.einsum("nij,nj->ni", np.maximum(FR, 0)[None] * (1 - J), w)
        restless = np.maximum(0, 0.5 - peace)[:, None] * -2 * centre(tgrad)
        dAs = np.stack([P["zeta_a"] * felt * (SE - P["eps0"]), conf_a[:, None] * (nic - a_) * np.ones((N, 1)),
                        P["xi_a"] * (obs - a_), P["eps_v"] * (z - y) * (1 + P["tw_want"] * np.minimum(B + TWo, 2.0))[:, None]
                        + P["resign"] * np.maximum(0, -delta)[:, None] * aligned[:, None] * (z - y),
                        times, P["fb_disc"] * disc, P["fb_acc"] * settle_, P["fb_peace"] * restless,
                        P["g_want"] * np.einsum("ng,ngc->nc", gs * np.select([gk == 0, gk == 1, gk == 2], [1.0, 0.7, 0.5], 0.0),
                                                gm - a_[:, None, :]) if GON else np.zeros((N, C)),   # v7: dreams and plans shape the want
                        P["hz_want"] * fhz[:, None] * (HZW - a_)], 1)                  # v7: time felt short shifts what one wants
        dA = dAs.sum(1)
        gap = 0.5 * np.abs(a_ - w).sum(1)
        gap_r = gap
        stress += P["gap_stress"] * gap
        # pent-up demand: each time the wanted option is blocked (closed, unnoticed, out-pulled) or fails,
        # the gap between wanted and actual adds pressure. Inertia, the strength with which the person holds
        # the colors the want would take from them, sets how much pressure it takes to break through.
        # satisfaction (meta variable, Emren 2026-10-04): needs met, compared with what the person has got used to,
        # recent luck, and the distance from the person they want to be (ideal-self gap: dejection, Higgins 1987)
        f_need = (nimp * need).sum(1) / nimp.sum(1)                # v6: needs weighted by how much they matter now
        react_eff = 1 + TON * (react - 1)
        mood = mood * 0.9 + 0.1 * react_eff * np.where(idle, 0.0, fdelta)
        smid = smid + (SMID[stage] - smid) / (52 * P["mid_years"]) if P["mid_years"] > 0 else SMID[stage]
        # v7 unmet hope (point 9): the young count on more than life gives them now and raise their hopes with what it
        # gives; as time starts to feel short, what has not come weighs on them and they let it go. The weight peaks in
        # midlife and fades as hopes are let go (Schwandt 2016; Heckhausen et al. 2010)
        hzf = np.minimum(1.0, (fhz / P["hope_hz"]) ** 2)
        hope += P["hope_up"] / 52 * (1 - hzf) * np.maximum(0, lvl + P["hope_young"] - hope)
        hope -= P["hope_let"] / 52 * hzf * np.maximum(0, hope - lvl)
        unmet = np.maximum(-1.0, (hope - lvl) / P["hope_young"])      # share of a young person's extra hope still unmet;
                                                                        # below 0, life gives more than is now hoped for
        gap_c = gap
        if P["gap_move"]:   # gap_move: a gap one is acting to close weighs less (progress toward a goal, not only its distance)
            dir_ = np.maximum(a_ - w, 0); ds_ = dir_.sum(1)
            al_ = np.where(ds_ > 1e-9, (hist_m * dir_).sum(1) / np.maximum(ds_, 1e-9), 0.2)   # recent acts toward the want
            gap_c = gap * (1 - P["gap_move"] * _uclip((al_ - 0.2) / 0.3, 0, 1))
        c_now = 1 / (1 + np.exp(-(P["sat_need"] * (f_need - smid) + P["sat_adapt"] * (f_need - lvl)
                                  + P["sat_mood"] * mood - P["sat_gap"] * (gap_c - P["sat_gap_ref"])
                                  + TON * P["sat_base"] * (base_mood - P["base_ref"])      # a person's own usual mood
                                  - P["regret_k"] * regret                                  # v7: lost dreams that still fit
                                  - (P["sat_hope"] * hzf * unmet if P["sat_hope"] else 0.0)
                                  + (float(np.interp(age, MU_A, MU_F)) if P["mind_u"] is not None else 0.0))))   # F19: the midlife dip, the later rise
        content += (c_now - content) / P["meta_weeks"]            # felt over the last months, not this week
        lvl += (f_need - lvl) / P["adapt_weeks"]                  # hedonic adaptation, incomplete by design
        # pent-up demand (discontent): wanting that is blocked (closed, unnoticed, out-pulled) or fails, while the
        # gap is beyond what people tolerate and they are not content, builds pressure (crystallisation of discontent)
        base_now = SP_[stage] * np.where(stage == 0, min(1.0, age / 8), 1.0)
        frus = has & (lost_open | lost_seen | pulled | (tried & ~succ))
        # pressure piles up faster when ordinary change is slow (low plasticity): youth mostly just changes
        stuck = 1 - base_now / SP_.max()
        Q = Q * (1 - P["q_decay"]) + np.maximum(0, gap - P["q_tol"]) * frus * (1.5 - content) * stuck
        rsh = np.einsum("nk,nkc->nc", held * I, prof)
        if BAT:   # vows, debts and promises hold their colors as a role does
            rsh = rsh + P["bind_hold"] * np.minimum(bind_m, 1)[:, None] * bind_c
        rs_ = rsh.sum(1, keepdims=True)
        hold = 0.4 * kw + 0.3 * habit / np.maximum(habit.sum(1, keepdims=True), 1e-9) + \
            0.3 * np.where(rs_ > 0, rsh / np.maximum(rs_, 1e-9), 0.2)
        if GON:   # v7: a passion holds its colors, as a role does
            pas = np.einsum("ng,ngc->nc", gs * (gk == 1), gm); ps_ = pas.sum(1, keepdims=True)
            hp_ = P["pass_hold"] * np.minimum(1, ps_)
            hold = (1 - hp_) * hold + hp_ * np.where(ps_ > 0, pas / np.maximum(ps_, 1e-9), 0.2)
        give = np.maximum(0, w - a_); give /= np.maximum(give.sum(1, keepdims=True), 1e-9)
        hold_against = 5 * (give * hold).sum(1)            # 1 = holds them as much as an even share

