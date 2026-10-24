# run_09_week.py: part 9 of 18 of engine._run, the life loop.
# The week loop begins: who is still at home, the outside push, the "week" pause.
# Lines here are _run's own, unchanged and at their own indent: engine.py joins the parts in order (engine.RUN_PARTS)
# and compiles them as one, so a name used here may be set in an earlier part. Never import or run it alone.
    for t in range(T):
        age = t / 52.0
        z = bound_logratios(z, P["min_color"], P["max_color"]); y = bound_logratios(y, P["min_color"], P["max_color"])
        if t % 13 == 0:   # the colours each quarter (conditions: rise, above_yrs, pair_yrs)
            w_q[w_qi % 40] = softmax(z); w_qi += 1
        if age > 12 and t % 52 == 0:                                   # nobody stays perfectly unbiased
            w0_ = softmax(z); flat = (w0_.max(1) - w0_.min(1)) < P["min_spread"]
            if flat.any():
                z[flat, w0_[flat].argmax(1)] += 0.1; z[flat] = centre(z[flat])
        nk_ = held[:, KID] & ~kid_on                                  # R15: the first child, however the children came
        alive[nk_, 5] = np.maximum(alive[nk_, 5], 1); kid_last[nk_] = t; kid_on = held[:, KID].copy()
        kids = held[:, KID] & (t - (kid_last if OR_ON else since[:, KID]) < 20 * 52) & ((alive[:, 5] > 0) | (not BAT))   # children
        # still at home (F7, one_roll: until the youngest is grown; before, the first)
        load = held * LOAD
        load[:, KID] = np.where(kids, LOAD[KID], 0.05 * held[:, KID])
        res[:, TIM] = _uclip(1 - load.sum(1) - 0.3 * (stage == 0), 0.05, 1)
        if RON:   # a title's own hours (a nurse's shifts, a councillor's evenings)
            res[:, TIM] = _uclip(res[:, TIM] + r_has[:, :NT_] @ GR["meets_res"][:, TIM], 0.05, 1)
        if WON and age >= 3:   # the world: the hours of one's own groups that no commitment counts (clubs, a movement)
            res[:, TIM] = _uclip(res[:, TIM] + WL.group_time(held, COM, FAI), 0.05, 1)
        if RON and MIS_ON and t % 52 == 0:   # v10: status held (summits, standings: hubris) and expertise by color (skills, careers)
            hub_ = r_has[:, :NT_][:, TIER_[:NT_] == 2].sum(1) + 0.5 * r_has[:, NT_:][:, PKIND_ == 2].sum(1)
            xp_ = (p_lev * (PKIND_ == 0)) @ WAYS_[NT_:] + np.minimum((t - r_since[:, :NT_]) / 520, 1) * r_has[:, :NT_] @ (WAYS_[:NT_] * CAREER_[:, None])
        w = softmax(z)
        if WON:   # the world's week first: its society, the cast, settings and place of each life (they read last week's person)
            if RON:   # the sector of the career held (sector= on careers) and the standing its titles give (standing=)
                sec_w = np.where(r_has[:, :NT_] & (W_SEC_ >= 0), W_SEC_, -1).max(1)
                st_w = np.where(r_has[:, :NT_] & (W_STD_ >= 0), W_STD_, 0).max(1)
            if RON and len(W_SDI_):   # each domain's standing from the titles held (one level 0-3 per domain)
                st_t_ = r_has[:, W_SDI_] * W_STD_[W_SDI_]
                dst_w = np.stack([np.where(W_SDOM_ == d_, st_t_, 0).max(1) for d_ in range(len(WLM.WK.DOMAINS))], 1)
            if BT_ON and RON and len(BT_TI):   # body_trust: the body each life holds a job at (a year there lifts its trust)
                WL.PP.bt_kind[:] = np.where(r_has[:, BT_TI], BT_TK[BT_TI][None], -1).max(1)
            if WA_ON:   # the world answers: the goal pursued (E1; an aim's face where a goal reads as one), and who is Known
                WL.PP.wa_goal(np.where((gal >= 0)[..., None], AIM["face"][np.maximum(gal, 0)], gm) if AIM_ON else gm, gd, gs, gb)
                if WA2_ON:   # F1: Known (aims v1's heights; without them, rung 4 or a title's standing), while the standing holds
                    rg_ = np.floor(np.asarray(WL.PP.rung)).max(1) if hasattr(WL.PP, "rung") else np.zeros(N)
                    sw_ = st_w if RON else np.zeros(N)
                    hold_ = (rg_ >= 3) | (sw_ >= 1) | ((r_has[:, HT_I[0]].any(1) if len(HT_I[0]) else False) if HT_ON else False)
                    kn_ = (ht_t[:, 0] >= 0) if HT_ON else ((rg_ >= 4) | (sw_ >= 1))
                    # wa_nat_climb: a seat held or a national name (recognition) is Known too; a voice alone is not
                    nk_ = WL.nat.known() if NAT_ON else False; nl_ = WL.nat.national() if NAT_ON else False
                    WL.PP.wa_set_known(((kn_ & hold_) | nk_) & ~dead, np.asarray(WL.gov_office, bool) | nl_, t)
                    hp_, sp_ = WL.PP.wa_price()   # F6: the phase's hours, and its stress in a busy season (monthly)
                    res[:, TIM] = _uclip(res[:, TIM] - hp_, 0.05, 1)
                    if t % 4 == 0:
                        stress = stress + sp_
            if LAND_ON and WL.land.play:   # v25 lane D: the land ways' hours a week (as the phase's price)
                res[:, TIM] = _uclip(res[:, TIM] - WL.land.hours * WL.land.E["way_time"], 0.05, 1)
            WL.week(t, dict(w=w, held=held, res=res, stress=stress, outlook=outlook, attr=attr, dead=dead, lens=softmax(k),
                            partner_same=partner_same if ID2 else None, sector=sec_w if RON else None,
                            title_standing=st_w if RON else None, children=alive[:, 5].copy(),   # the cast keeps every child
                            domain_standing=dst_w if RON and len(W_SDI_) else None,
                            gov_office=r_has[:, W_GOV_].any(1) if RON and W_GOV_ else None,
                            head_gov=r_has[:, W_HOG_] if RON and W_HOG_ >= 0 else None,
                            lead_has=(np.where(LW_T_ >= 0, r_has[:, np.maximum(LW_T_, 0)], False) if LW_ON else None)))
            if LAND_ON:   # v25 lane D: the land's week on the lives (strikes, the years after, the dose, sick land, worry)
                lf_ = WL.land.take(); need += lf_[0]; mood = mood + lf_[1]; stress = stress + lf_[2]
                res[:] = _uclip(res + lf_[3], 0, 1)
                for n_, x_ in WL.land.drain():
                    if n_ in events:
                        events[n_].append(dict(land=x_))
            if TW_ON and getattr(WL.PP, "tilt_ver", 0) != tw_ver:   # v25 #10: r as the year's rungs computed it (the game's)
                tw_ver = WL.PP.tilt_ver; prizes = WF.prizes(WL.PP); prizes_moves = WL.PP.tilt_moves
            if LW_ON and WL.PP.lw_lost:   # S7: an office the post's end took (a fall, a term, a hand-over, a move)
                for n_, i_, why_ in WL.PP.lw_lost:
                    if LW_T_[i_] >= 0:
                        r_lose(n_, int(LW_T_[i_]), "the post " + why_)
                WL.PP.lw_lost = []
            for n_ in np.nonzero(WL.office_lost)[0]:   # W40: the government fell, and their office with it
                for i_ in W_GOV_:
                    r_lose(n_, i_, "the government fell")
            ei_, ep_, ek_ = WL.era()
            era_i[t], era_p[t], era_k[t] = ei_, ep_, ek_
            if WL.W.era_key != getattr(WL, "_era_key", None):   # an era begins: everyone hears its message (4b)
                WL._era_key = WL.W.era_key
                if WL.W.era_key in COMBO_MIX:
                    era_at[t] = (WL.W.era_key, ei_, ERA_KINDS[ek_])
            drv_h = WL.harsh_n; drv_u = float(WL.W.unrest); drv_p = float(WL.W.prosper)
            alive[:, :5] = WL.PP.alive
            if ID2:   # how strict the people around each person are with the role expected, and how far they accept a named gender
                RS0, AT0 = WL.role_norms()
            clim_w = WL.climate()   # how hostile the place and one's people are to being out (replaces climate + faith)
            if events:   # the world in the story (Emren 10:42): big public events always, the rest when they touch the character
                # or their people; and the cast's own events (the birth, people entering, wants), from the first week on
                for n_, lst_ in WL.story(list(events), dead).items():
                    events[n_].extend(dict(world=e_) for e_ in lst_)
                world_cast(WL.drain())
            else:
                WL.drain()
        if RX_ON:   # v25 lane C: a new week's demands and responses; a clash waiting for its moment is brought (after the
            RX.week_reset()   # world's week, which set this week's forced moments)
            if CL_ON:
                RX.clash_week(t, WL)
            if SK_ON:
                RX.seek_week(t, WL, age)
        if t % record_every == 0:
            if GG_ON:
                grey_y.append(WL.W.sph_grey()[np.asarray(WL.PP.loc)].astype(np.float32))
            W_hist.append(w.copy()); M_hist.append(M.copy()); S_hist.append(stage.copy()); A_hist.append(softmax(y))
            R_hist.append(res.copy()); K_hist.append(held * np.maximum(I, 1e-3))
            if DOM_ON:
                D_hist.append(Dz.astype(np.float32))
            V_hist["acc"].append(plast * ctrl); V_hist["core"].append(softmax(k)); V_hist["SE"].append(SE.copy())
            V_hist["habit"].append(habit / np.maximum(habit.sum(1, keepdims=True), 1e-9))
            V_hist["role"].append(np.einsum("nk,nkc->nc", held * I, prof))
            V_hist["ctrl"].append(ctrl.copy()); V_hist["plast"].append(plast.copy()); V_hist["Q"].append(Q.copy())
            V_hist["content"].append(content.copy()); V_hist["peace"].append(peace.copy()); V_hist["skill"].append(sig.copy())
            V_hist["need"].append(need.copy()); V_hist["adj"].append(adj[:, :NA_OUT].copy())
            V_hist["adj_v"].append((adj_v * ADJ_SIDE)[:, :NA_OUT] if adj_v is not None else np.full((N, NA_OUT), np.nan))
            for nm_, v_ in (("fneed", f_need), ("mood", mood), ("stress", stress), ("cload", cload), ("tension", tension),
                            ("react", react), ("steady", steady), ("base_mood", base_mood), ("outlook", outlook), ("gap", gap_r),
                            ("wound", wound), ("support", support), ("trouble", trouble), ("fortune", fortune), ("horizon", fhz), ("discipline", dsc), ("lvl", lvl), ("q_rel", q_rel), ("unmet", unmet), ("hope_w", hzf * unmet), ("threat", thr), ("scar", scar.sum(1))):
                V_hist[nm_].append(np.broadcast_to(v_, (N,)).copy())
            V_hist["doors"].append(doors(nic, res)); A_src.append(asrc.astype(np.float32)); V_hist["chan"].append(chan.astype(np.float32))
            if HM_ON:   # v22.5 F1: the two halves of health
                V_hist["body"].append(body_v.copy()); V_hist["mind"].append(mind_v.copy())
            for kk_, nm_ in enumerate(("n_dream", "n_passion", "n_plan")):
                V_hist[nm_].append((gk == kk_).sum(1))
            V_hist["harmonious"].append(np.where((gk == 1).any(1), (ga * gs * (gk == 1)).sum(1) / np.maximum((gs * (gk == 1)).sum(1), 1e-9), np.nan))
            V_hist["regret"].append(regret.copy())
            V_hist["n_titles"].append(r_has[:, :NT_].sum(1) if RON else np.zeros(N, int))
            V_hist["n_perks"].append(r_has[:, NT_:].sum(1) if RON else np.zeros(N, int))
        if intervention is not None:
            y0_ = y.copy(); intervention(t, P, nic, y); asrc[:, 6] += y - y0_
        if UPL_ON:   # F15: the start's lean, full to up_from, then fading by half every up_half years
            upf_ = 1.0 if age < P["up_from"] else 0.5 ** ((age - P["up_from"]) / P["up_half"])
            upe_ = 1 - P["up_ease"]                       # how much of the setup's own society pulls
            if P["up_lean"]:
                a_ = softmax(y)
                dy_ = (P["up_lean"] * up_short(a_))[:, None] * centre(5 * (UPM_ - a_))
                if age >= P["up_from"]:
                    dy_ = dy_ - UP_DEC * up_oy
                up_oy += dy_
                y = y + dy_; asrc[:, 1] += dy_
        if EP_ON:
            ep_now[:] = -1   # no return yet this week (set after the situation pause, read from the choose pause on)
        if IW_ON:   # N3: no setback yet this week
            iw_fact[:] = -1; iw_why[:] = [None] * N
        if NW_ON:   # need_why: a new week's record (what the caller changes at the "week" pause is the player's)
            nw[:] = 0; nw_imp[:] = -1; nw_imp_cause[:] = -1; nw_prev[:] = need
        if pausing:
            _pause_state(pz_st, ST_CELLS, ST_FR)
            _ = yield Pause("week", t, pz_st, None)
            pz_st._fr = None
            if NW_ON: nw_mark(NW_PLAYER)
            if SCN_ON and scn_cast:   # the scenario harness's cast (P["scn"]): set before the week's reactions
                for n_, mx_ in RX.apply_cast(list(scn_cast)):
                    z[n_] = centre(np.log(np.maximum(mx_, 1e-4))); k[n_] = z[n_].copy(); w[n_] = softmax(z[n_])
                scn_cast.clear()
            if SCN_ON and scn_hazard:   # v25 lane D, the scenario hook: the caller's hazards and harvests, this week
                WL.scn(list(scn_hazard)); del scn_hazard[:]
                if LAND_ON:
                    lf_ = WL.land.take(); need += lf_[0]; mood = mood + lf_[1]; stress = stress + lf_[2]
                    res[:] = _uclip(res + lf_[3], 0, 1)
                    for n_, x_ in WL.land.drain():
                        if n_ in events:
                            events[n_].append(dict(land=x_))
            if WFX_ON:
                wfx = [[] for _ in range(N)]
        e_i, e_p = era_i[t], era_p[t]
        f_w = P["world_pos_k"] * (np.asarray(WL.W.Pos, float) - 0.2) if WON else P["f_world"]   # what the order rewards
        if UPL_ON and P["up_ease"]:   # F15: the setup's society is a lean too (world_profile toward even)
            WP_ = 0.2 + upe_ * (np.asarray(P["world_profile"], float) - 0.2)
            if not WON:
                f_w = upe_ * np.asarray(f_w, float)
        if STH_SOC is not None:   # v22.5, F12: and what the start's society rewards
            f_w = (1 - P["start_soc"]) * f_w + P["start_soc"] * STH_FW
        f_tot = f_w[None, :] + P["lam_local"] * (nic - 0.2) * (np.asarray(WL.PP.msg_w, float)[:, None] if WON else 1.0) \
            + P["era_world"] * e_i * (e_p - 0.2)   # msg_w: how strongly one's groups and people pull (1 typical, spec 3 §1.4)
        if age < 3:
            continue
        stress0 = stress.copy()                        # reactivity scales whatever adds stress this week
        if BAT and not WON and t % 52 == 0 and age > 12:   # grandparents of grown children die outside the story (the Library writes it for childhood)
            alive[:, 3] = rng.binomial(alive[:, 3].astype(int), 1 - min(1, P["mort"][0] * np.exp(P["mort"][1] * (age + 55))))
        if BAT and t % 4 == 0:   # each month: which inner moments, echoes and life-event gates hold for each person
            alive[:, 4] = held[:, PAR]
            cond_hold += cond_ok * (stage >= 2)[:, None]; cond_n += (stage >= 2)
            back_ = (friend_back > NEVER // 2) & (t >= friend_back); alive[back_, 2] = 1; friend_back[back_] = NEVER
            ns = cond_ns(t, age, w)
            memo_ = {}   # speed pass: within this month a condition's text gives the same answer (none draws chance here)
            for c_ in L["COND"]:
                if c_["kind"] in (2, 4):   # an echo comes through its anchor, a return moment only as a pick's return
                    continue
                cond_ok[:, c_["s"]] = ev_memo(c_["req_off"] if FM_OFF_ and "req_off" in c_ else c_["req"], ns, memo_)
                cond_fac[:, c_["s"]] = factor(c_, ns, memo_) * P["inner_w"] if c_["kind"] == 1 else factor(c_, ns, memo_)
            if ID2:   # N1b: intimacy comes less often to an asexual person; a same-sex couple has a baby only as planned;
                # an intersex person's own pregnancy or fathering is rarer (a moment without a condition starts from 1)
                for si_ in INTIM_:
                    cond_fac[:, si_] = (cond_fac[:, si_] if si_ in COND_S else 1.0) * np.where(ace, P["ace_intim"], 1.0)
                if BABY_ >= 0:
                    ok_ = ~(held[:, PAR] & partner_same) | ((gk == 2) & (gd == KID)).any(1)
                    f_ = np.where(intersex, P["intersex_fert"], 1.0)
                    if BABY_ in COND_S:
                        cond_fac[:, BABY_] *= f_; cond_ok[:, BABY_] &= ok_
                    else:
                        cond_fac[:, BABY_] = f_ * ok_
            for e_, c_ in enumerate(ECH):
                newa = (echo_anchor[:, e_] <= NEVER // 2) & ev_cond(c_["anchor"], ns)
                if np.count_nonzero(newa):   # the clock starts; only some anchors ever come back (the rest just hold the slot a while)
                    ii_ = np.nonzero(newa)[0]; lo_, hi_ = c_["delay"]
                    echo_anchor[ii_, e_] = t; echo_end[ii_, e_] = t + int((hi_ + 2) * 52)
                    echo_due[ii_, e_] = np.where(rng.random(len(ii_)) < P["echo_p"] * ECH_R[e_], t + rng.uniform(lo_, hi_, len(ii_)) * 52, 10 ** 9)
                old_ = (echo_anchor[:, e_] > NEVER // 2) & (t > echo_end[:, e_])
                echo_anchor[old_, e_] = NEVER
                pend = (echo_anchor[:, e_] > NEVER // 2) & (t >= echo_due[:, e_])
                echo_ready[:, e_] = False
                if np.count_nonzero(pend):
                    ns["sa"] = ys_ = np.where(pend, (t - echo_anchor[:, e_]) / 52, 0.0)
                    echo_ready[:, e_] = pend & ev_cond(c_["req"], ns)
                    echo_fac[:, e_] = factor(c_, ns)

