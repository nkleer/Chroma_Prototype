# run_18_integrate.py: part 18 of 18 of engine._run, the life loop.
# 5 to 8. integrate, rites, conversion, breakthrough, the "end" pause, the outputs.
# Lines here are _run's own, unchanged and at their own indent: engine.py joins the parts in order (engine.RUN_PARTS)
# and compiles them as one, so a name used here may be set in an earlier part. Never import or run it alone.
        # ---- 5. integrate. Plasticity belongs to the life stage
        if P["tw_trans"]:   # a turning point this week opens a window (see tw_trans)
            if tw_held is None:
                tw_held = held.copy(); tw_has = r_has[:, :NT_].copy() if RON else None
            tr_ = (held != tw_held).sum(1) + ((r_has[:, :NT_] != tw_has).sum(1) if RON else 0)
            if P["tw_sep"]:
                TWo += P["tw_trans"] * np.minimum(tr_, 2) * (stage >= 1)
            else:
                B += P["tw_trans"] * np.minimum(tr_, 2) * (stage >= 1)
            tw_held = held.copy()
            if RON: tw_has = r_has[:, :NT_].copy()
        base = SP_[stage] * np.where(stage == 0, min(1.0, age / 8), 1.0)
        settle = np.log1p(M / P["M0"]) if P["settle_log"] else M / P["M0"]   # experience settles a person, with diminishing effect
        s_eff = P["steady_cap"] * np.tanh(steady / P["steady_cap"])          # steadiness slows change, up to a ceiling
        plast = base / (1 + settle) * (1 + B) / (1 + TON * P["steady_k"] * s_eff)   # a steady person changes more slowly
        if SET_ON:   # F14: colours settle with age; a big event (openness) still lets them move as a younger person's
            sf_ = float(np.interp(age, SET_A, SET_F))
            settle_f = sf_ + (1 - sf_) * _uclip((B - set_bu) / P["set_big"], 0, 1)
            set_bu += (B - set_bu) / (52 * P["set_usual"])
            plast = plast * settle_f
        F = np.stack([centre(dI), centre(dV), centre(dS), centre(dC), centre(dU)], 1)
        noise = centre(rng.normal(0, P["noise"], (N, C)))
        if P["drift_k"] != 1.0:   # played lives: the game weighs the random drift
            noise = P["drift_k"] * noise
        if CUR_ON:   # item 12: the current takes over part of the random drift
            noise = (1 - P["cur_cut"]) * noise
        support =0.5 * (need[:, NIDX["belonging"]] + res[:, TIE])          # being cared for: belonging and ties
        if WON:   # and what the cast and the settings give in hard weeks
            support = support + np.asarray(WL.PP.support, float)
        open_ = np.minimum(wound, 2.0)
        kap_e = P["kappa_e"] * (1 + P["care_k"] * support + P["heal_k"] * open_ * support)   # cared for, people come back
        if P["tw_pull"]:   # while a window is open, the old self pulls back less
            kap_e = kap_e / (1 + P["tw_pull"] * np.minimum(B + TWo, 2.0))
        drift = plast[:, None] * noise + P["mom"] * v - kap_e[:, None] * (z - k)
        if P["hz_self"]:   # next version: limited time felt changes who one is as it changes what one wants
            drift = drift + P["hz_self"] * fhz[:, None] * centre(HZW[None] - w)
        stepF = plast[:, None, None] * F
        if P["tw_force"] and P["tw_sep"]:   # an open window: what happens now moves the colors more
            stepF = stepF * (1 + P["tw_force"] * np.minimum(TWo, 2.0))[:, None, None]
        if SEA_ON and sea_tr.any():   # the season's transforming chance moves the colors further
            stepF = stepF * np.where(sea_tr, P["season_amp"], 1.0)[:, None, None]
        chan[:, :5] += stepF; chan[:, 6] += drift
        dz_ = stepF.sum(1)
        if UPL_ON and P["up_self"]:   # F15: the start's lean on who they are (booked as social)
            udz_ = (P["up_self"] * up_short(w) * plast)[:, None] * centre(5 * (UPM_ - w))
            if age >= P["up_from"]:
                udz_ = udz_ - UP_DEC * up_oz
            up_oz += udz_
            dz_ = dz_ + udz_; chan[:, 2] += udz_
        if DOM_ON:   # a share of what a moment in an area teaches stays in that area; offsets fade back toward the core
            srf_ = P["dom_share"] * dz_ * (inA_ & ~idle)[:, None]
            Dz[ar, np.maximum(area_, 0)] += srf_; dz_ = dz_ - srf_
            hl_ = np.array([held[:, CAR] | (stage <= 2), np.ones(N, bool), np.ones(N, bool), held[:, FAI]]).T   # school is work
            Dz *= (1 - np.log(2) / (52 * np.where(hl_, P["dom_half"], P["dom_end_half"])))[:, :, None]
            Dz = np.clip(Dz - Dz.mean(2, keepdims=True), -P["dom_cap"], P["dom_cap"])
        if WON and t % 4 == 0:   # S2 (read only, for the game): the colour shares of what surrounds them, once a month
            around = WL.PP.around()
        if CUR_ON and t % 4 == 0 and age >= 3:   # item 12: the times as a steady current, once a month
            if WON:
                cl_, st_, tm_ = (np.asarray(x_, float) for x_ in WL.PP.cur_parts)
                if SOC_OWN:   # soc_own: the close people are partly the company they pick
                    cl_ = (1 - SOC_OWN) * cl_ + SOC_OWN * onic
            else:   # no outer world: the niche stands for people and places (the circle's turnover is random)
                cl_, st_ = nic, nic
                wp_ = WP_ if UPL_ON and P["up_ease"] else np.asarray(P["world_profile"], float); tm_ = wp_ + 0.5 * e_i * (np.asarray(e_p, float) - wp_)
                tm_ = np.broadcast_to(tm_ / tm_.sum(), (N, C))
            cm_ = P["cur_mix"]
            cur_ = (cm_[0] * cl_ + cm_[1] * st_ + cm_[2] * tm_) / sum(cm_)
            cur_m = cur_.copy() if cur_m is None else cur_m + (cur_ - cur_m) / (12 * P["cur_mem"])   # what has reached them lately
            cur_ = cur_m
            b0_, pk_, at_, wd_ = P["cur_age"]
            if WON and P["cur_rel"]:   # against the society (people), the town's average places, the times with cur_era of the era
                V_ = np.asarray(WL.W.V, float)[None, :]
                pr_ = WL.PP.places_ref if getattr(WL.PP, "places_ref", None) is not None else V_
                ref_ = (cm_[0] * V_ + cm_[1] * pr_ + cm_[2] * (P["cur_era"] * V_ + (1 - P["cur_era"]) * tm_)) / sum(cm_)
                lr_ = np.log(np.maximum(cur_m, 1e-4)) - np.log(ref_) - P["cur_bal"] * np.log(np.maximum(w, 1e-4))
                cdz_ = (P["cur_rel_k"] * (b0_ + pk_ * np.exp(-((age - at_) / wd_) ** 2)) * plast)[:, None] * centre(lr_)
            else:
                cdz_ = (P["cur_k"] * (1.0 if WON else P["cur_off"]) * (b0_ + pk_ * np.exp(-((age - at_) / wd_) ** 2)) * plast)[:, None] * centre(5 * (cur_ - w))
            if P["era_push_k"] != 1.0:   # played lives: the game weighs the times' push as it weighs an era's
                cdz_ = P["era_push_k"] * cdz_
            if P["cur_will"]:   # cur_will: on a colour wanted beyond what is held, the current pulls it down up to this share less
                cdz_ = centre(np.where(cdz_ < 0, cdz_ * (1 - P["cur_will"] * _uclip(5 * (softmax(y) - w), 0, 1)), cdz_))
            dz_ = dz_ + cdz_; chan[:, 8] += cdz_; cur_sum += np.abs(cdz_).sum(1)
        if ODD_ON_ and t % 4 == 0:   # S4: blending in at a place steps the colours toward it (booked with the current)
            edw_ = WL.PP.eyes_dw
            if edw_.any():
                edz_ = centre(5 * edw_); WL.PP.eyes_dw = np.zeros_like(edw_)
                if SET_ON: edz_ = settle_f[:, None] * edz_   # F14
                dz_ = dz_ + edz_; chan[:, 8] += edz_
        if MK_ON and t % 4 == 0:   # spheres phase 2: the mark of the work, a year's step once it is drawn (booked with the current)
            mdw_ = WL.PP.mark_dw
            if mdw_.any():
                mdz_ = centre(5 * mdw_); WL.PP.mark_dw = np.zeros_like(mdw_)
                if P["era_push_k"] != 1.0:   # played lives: weighed as the other outside pushes
                    mdz_ = P["era_push_k"] * mdz_
                if SET_ON: mdz_ = settle_f[:, None] * mdz_   # F14
                dz_ = dz_ + mdz_; chan[:, 8] += mdz_
            hu_ = WL.PP.mark_hurt & ~dead
            if hu_.any():   # a serious injury at work
                res[hu_, HEA] -= 0.15; WL.PP.mark_hurt = np.zeros(N, bool)
            for n_ in np.nonzero(WL.PP.mark_die & ~dead)[0] if P["self_death"] else ():   # (deaths only where lives can die)
                die(int(n_), "an accident at work")
            WL.PP.mark_die = np.zeros(N, bool)
        z_new = centre(z + dz_ + drift)
        v = 0.7 * v + 0.3 * (z_new - z)
        if P["tw_pen"]:    # a big life event reaches the deep core directly, in proportion to how hard it hit
            k = k + (P["tw_pen"] * big * np.minimum(np.abs(delta) / np.maximum(stakes, 1e-9), 1.0))[:, None] * (z_new - z)
        z = z_new
        eps_w = eps_k * (1 + P["tw_core"] * np.minimum(B + TWo, 2.0)) if P["tw_core"] else eps_k   # open: the core follows faster
        k = k + (eps_w * (1 + P["harden_k"] * open_ * (1 - support)))[:, None] * (z - k)   # alone, the shift hardens into the core
        if SEA_ON and sea_tr.any():   # and what the person became in it settles into the deep core
            k = k + (P["season_imprint"] * sea_tr)[:, None] * (z - k)
        if P["core_walk"]:   # v6: the deep core itself drifts a little, unnoticed, so people grow apart over decades (12-year
            cw_ = ((stage >= 2) * settle_f)[:, None] if SET_ON else (stage >= 2)[:, None]   # (F14: settling with age)
            k += P["drift_k"] * P["core_walk"] * centre(rng.normal(0, 1, (N, C))) * cw_   # value stability ~.5: Leijen 2022)
        ystep = P["asp_rate"] * (SP_[stage] * (1 + B) / (1 + TON * P["steady_want"] * P["steady_k"] * s_eff))[:, None, None]
        if SET_ON:   # F14: what they want settles with age as who they are does
            ystep = ystep * settle_f[:, None, None]
        asrc[:, AS_WEEKLY] += ystep * (dAs - dAs.mean(-1, keepdims=True))
        y = centre(y + ystep[:, 0] * centre(dA))
        M += 0.1 * np.abs(delta) * stakes
        re_ = react_eff * (1 - P["hz_calm"] * np.minimum(fhz, 1)) if P["hz_calm"] else react_eff   # v7: calmer as time feels short
        if P["mind_kid"] is not None:   # F19: a child carries less of what adds stress in a week than an adult
            re_ = re_ * float(np.interp(age, MK_A, MK_F))
        stress = _uclip((stress0 + re_ * (stress - stress0)) * 0.93 + re_ * 0.08 * np.maximum(0, -fdelta), 0, 3)
        B *= decay_B; TWo *= decay_B
        nic += P["nu_niche"] * (np.where(idle[:, None], nic, ma) - nic) + 0.002 * ((WP_ if UPL_ON and P["up_ease"] else P["world_profile"]) - nic) + P["era_niche"] * e_i * (e_p - nic)
        if RP_ON and P["role_niche"]:   # role_practice: the people of one's commitments, in their ways
            rsum_ = rw_.sum(1, keepdims=True)
            nic += P["role_niche"] * P["nu_niche"] * rsum_ * (rw_ / np.maximum(rsum_, 1e-9) - nic)
        if P["turnover"]:   # v6: the people around you change: new colleagues, friends, neighbours bring their own ways
            new_ = rng.random(N) < 1 / (52 * P["turn_years"])
            moved = new_.astype(float)
            if new_.any():
                circle[new_] = random_messages(rng, int(new_.sum()))
            nic += P["turnover"] * turn_pm[:, None] * np.asarray(P["turn_stage"])[stage][:, None] / 52 * (circle - nic)
        if WON:   # the world: the niche is what the settings and the close circle bring, with the times through them
            if SOC_OWN:   # soc_own: the company they pick follows what they do, as the niche does with the world off
                onic += P["nu_niche"] * (np.where(idle[:, None], onic, ma) - onic)
            nic = np.array(WL.PP.niche, float)
            if STH_SOC is not None:   # v22.5, F12: and the start's society
                nic = (1 - P["start_soc"]) * nic + P["start_soc"] * STH_SOC

        for i in log_lives:
            if not idle[i]:
                more_ = dict(threat=round(float(thr[i]), 2))
                if ID2 and act_cw[i] > 0:
                    more_["cross"] = round(float(act_cw[i]), 2)   # N1b: the act crossed the role expected of them (people frowned)
                if MIS_ON:
                    more_["misread"] = round(float(mis_[i, a[i]]), 2)   # logit the felt odds were bent by (+ hopeful, - fearful)
                if WON and W_WHO_[s[i]]:   # who is in the moment: the cast member with the want first, else by role
                    more_["who"] = WL.who(i, int(s[i]))
                    if BO_ON and bo_seed[i] >= 0:   # bold ways: the seed keeps who was in its moment (a link may find them gone)
                        ep_seeds[bo_seed[i]]["who"] = more_["who"]
                if WON and EYES_ON_ and EYEW_[s[i]]:   # S3, S4: the places of a caught-between or odd-one-out moment
                    ei_ = WL.eyes_info(i, int(s[i]))
                    if ei_:
                        more_["eyes"] = ei_
                if WON and LEADS_ON_ and LEADS_[s[i]] and getattr(WL, "lw", False):   # S7: the post the moment is about
                    li_ = WL.lead_info(i, int(s[i]))                                     # (its {place}, way, legitimacy)
                    if li_:
                        more_["lead"] = li_
                if SAC_ON_ and SACS_[s[i]]:   # S5: the line, the offer ({offer}), its round, size and refusal odds
                    si_ = WL.sacred_info(i, int(s[i]))
                    if si_:
                        more_["sacred"] = si_
                if WON and FARS_ON_ and FARS_[s[i]]:   # far_ties: the tie's town and what happened there
                    fi_ = WL.far_info(i, int(s[i]))
                    if fi_:
                        more_["far"] = fi_
                if SEEN_ON:   # S6: per option, the Library's word and the strongest model on its path, else its way
                    sn_ = WL.seen_info(i, int(s[i]))
                    if sn_:
                        more_["seen"] = sn_
                if WON:   # the world on the options (hooks §2.6, §2.8): each option's lever and where it lands; a move names towns
                    lv_ = WL.option_levers(int(s[i]))
                    if lv_:
                        more_["levers"] = lv_
                    if WL.move_s[s[i]] and hasattr(WL.PP, "move_options"):
                        more_["places"] = WL.PP.move_options(i)
                best_, bm_ = None, P["epi_recall"]
                mc_ = ma[i] - ma[i].mean(); nm_ = float(np.linalg.norm(mc_)) + 1e-9   # the act's lean among the colors
                for ep_ in epi[i]:
                    if t - ep_["last"] < 26:
                        continue
                    hl_ = P["mem_pos"] if ep_["success"] else P["mem_neg"]   # fading affect bias (a scar's pull is its own state)
                    st_ = ep_["w"] * 0.5 ** ((t - ep_["t"]) / (52 * hl_))
                    cs_ = 1.0 if ep_["situation"] == L["names"][s[i]] else float(mc_ @ ep_["mix"]) / (nm_ * ep_["nm"])
                    mt_ = st_ * cs_ if cs_ >= 0.7 else 0.0   # the same moment again, or an act leaning the same way
                    if mt_ > bm_:
                        best_, bm_ = ep_, mt_
                if best_ is not None:
                    best_["last"] = t
                    more_["recall"] = dict(age=best_["age"], situation=best_["situation"], choice=best_["choice"],
                                           success=best_["success"], scar=best_["scar"], strength=round(bm_, 2))
                events[i].append(dict(age=round(age, 2), stage=STAGE_NAMES[stage[i]],
                                      situation=L["names"][s[i]], choice=L["labels"][s[i]][a[i]],
                                      success=bool(succ[i]), delta=round(float(delta[i]), 3),
                                      push={ch: stepF[i, j].round(4).tolist() for j, ch in enumerate(CHANNELS[:5])},
                                      w=softmax(z[i]).round(3).tolist(), want=softmax(y[i]).round(3).tolist(),
                                      wanted=L["labels"][s[i]][best[i]], res=res[i].round(2).tolist(),
                                      gate=(("lacked the means" if not open_r[i, best[i]] else "not offered") if lost_open[i] else "unnoticed" if lost_seen[i]
                                                                               else "pulled away" if pulled[i] else "chosen"),
                                      ctrl=round(float(ctrl[i]), 2), **more_))
                if abs(delta[i]) >= P["epi_min"]:   # an act that hit hard becomes an episode the person may recall later
                    epi[i].append(dict(t=t, last=t, age=round(age, 2), situation=L["names"][s[i]], choice=L["labels"][s[i]][a[i]],
                                       success=bool(succ[i]), scar=bool(P["scar_k"] and not succ[i] and stakes[i] >= P["scar_min"]),
                                       w=float(abs(delta[i])), mix=mc_.copy(), nm=nm_))
                    if len(epi[i]) > 60:
                        epi[i].sort(key=lambda e_: e_["w"] * 0.5 ** ((t - e_["t"]) / (52 * P["mem_neg"])))
                        del epi[i][0]

        # ---- 6. rites of passage: an impactful event inside the next stage's window
        nxt = np.minimum(stage + 1, NS - 1)
        lo, hi = STAGE_LO[nxt], STAGE_HI[nxt]
        progress = _uclip((age - lo) / np.maximum(hi - lo, 1e-9), 0, 1)
        impact = np.abs(delta) / stakes * L["RIT"][s, nxt]   # only situations that can mark this passage count
        # a big surprise in a fitting situation may mark the passage; readiness grows across the window
        p_rite = 1 - np.exp(-P["rite_h"] * impact ** 2 * (1 + P["rite_ready"] * progress ** 2))
        rite = (stage < NS - 1) & (age >= lo) & ((rng.random(N) < p_rite) | (age >= hi))
        for n in np.nonzero(rite)[0]:
            quiet = bool(age >= hi[n] and impact[n] < P["rite_thr"] * 0.2)
            k[n] += P["rite_imprint"] * (z[n] - k[n])     # who you are now becomes your anchor
            B[n] += P["rite_boost"]; eps_k[n] *= P["stiffen"]
            stage[n] += 1
            if sea_fits(int(stage[n]), age):
                sea_open(n, int(stage[n]))                # the threshold season of the stage just entered
            rec = dict(life=int(n), age=round(age, 2), to=STAGE_NAMES[stage[n]], quiet=quiet,
                       event=None if quiet else f"{L['names'][s[n]]}: {L['labels'][s[n]][a[n]]} ({'success' if succ[n] else 'failure'})",
                       w=softmax(z[n]).round(3).tolist())
            rite_log.append(rec)
            if n in events:
                events[n].append(dict(rite=rec))
            if GON:   # v7 (2A): a rite seals dreams that have proved themselves into passions
                seal(n, "a rite of passage")
                if stage[n] == 2:   # coming of age: a strong dream that is not yet a passion becomes a plan (Emren 21:39)
                    for j in np.nonzero(gk[n] == 0)[0]:
                        if (gk[n] == 2).sum() < P["max_plans"] and rng.random() < P["dream_plan"] * gs[n, j]:
                            to_plan(n, j)

        # ---- 7. conversion: dissonance past threshold
        w = softmax(z)
        openness = np.sqrt(base / 0.9)
        theta = P["theta0"] * (1 + 2 * w) / np.maximum(openness, 1e-3)[:, None]
        D = np.minimum(D, 1.5 * theta)
        over = D >= theta
        if over.any():
            for n, c in zip(*np.nonzero(over)):
                acc = _uclip(1 - 0.4 * FR[c], 0.2, 1.4); acc[c] = 0   # framing shapes where you can go
                q = obs[n] * SE[n] * acc; q = q / q.sum()
                dz = centre(P["Lam"] * (q - np.eye(C)[c]) * min(2.0, D[n, c] / theta[n, c]))
                z[n] += dz; k[n] += 0.5 * dz; chan[n, 5] += dz
                y[n] = centre(y[n] + 2 * dz)          # a turning point is first a change in what you want
                asrc[n, 4] += 2 * dz
                B[n] += P["crisis"]; D[n] = 0
                steady[n] *= 1 - 0.5 * TON                    # a crisis shakes who one is
                conv_log.append((int(n), t, int(c), q))
                if n in events:
                    events[n].append(dict(conversion=dict(age=round(age, 2), disowned=COLORS[c],
                                                          toward=q.round(2).tolist(), w=softmax(z[n]).round(3).tolist())))

        # ---- 8. breakthrough: pent-up demand overcomes inertia (stick, then slip)
        q_thr = P["q_theta"] * np.maximum(hold_against, 0.2) ** P["q_hold"]
        # v6 (fresh-start effect: Dai, Milkman & Riis 2014; Alter & Hershfield 2014): a birthday, an age ending in 9, or a
        # change of surroundings lowers the bar for a change that has been building
        lm = float(t % 52 == 0) + 0.3 * float(int(age) % 10 == 9) + moved
        q_thr = q_thr * (1 - P["landmark"] * _uclip(lm, 0, 1))
        brk = (Q >= q_thr) & (gap > P["q_min_gap"]) & (stage >= 2)
        for n in np.nonzero(brk)[0]:
            dz = centre(P["q_step"] * (y[n] - z[n]))
            w0 = softmax(z[n])
            z[n] += dz; k[n] += 0.5 * dz; chan[n, 7] += dz
            B[n] += P["q_open"]; Q[n] = 0.0; sh_brk[n] = t
            steady[n] *= 1 - 0.3 * TON
            nic[n] += P["q_niche"] * (softmax(y[n]) - nic[n])
            force_re[n] = True                              # the commitment that fits worst comes up for decision
            rec = dict(age=round(age, 2), gap=round(float(gap[n]), 2), hold=round(float(hold_against[n]), 2),
                       before=w0.round(3).tolist(), w=softmax(z[n]).round(3).tolist(), want=softmax(y[n]).round(3).tolist())
            brk_log.append((int(n), t, rec))
            if n in events:
                events[n].append(dict(breakthrough=rec))
        if BT_ON and t % 52 == 51:   # body_trust: each life's trust at the end of the year of age (NaN before 15 and once ended)
            bt_y[:, t // 52] = np.where(dead[:, None], np.nan, btrust)
        if pausing:
            _pause_state(pz_st, ST_CELLS, ST_FR)
            _ = yield Pause("end", t, pz_st, None)
            pz_st._fr = None
    z = bound_logratios(z, P["min_color"], P["max_color"]); y = bound_logratios(y, P["min_color"], P["max_color"])
    W_hist.append(softmax(z)); M_hist.append(M.copy()); S_hist.append(stage.copy()); A_hist.append(softmax(y))
    R_hist.append(res.copy()); K_hist.append(held * np.maximum(I, 1e-3))
    wout = WL.output(log_lives) if WON else None           # the outer world for the game (world-build.md, "Game data")
    pt_out = {}
    if WON and getattr(WL.PP, "pt_on", False):   # place_turnover (only when on): the world's closings and openings (pt_log,
        ptl_ = np.zeros((N, int(years)), np.int64)   # burn-in included, q in the world's quarters) and how many of each
        for n_, t_ in WL.PP.pt_hits:                 # life's haunts closed in each year of the run
            y_ = (int(t_) - WL.t0) // 52
            if 0 <= y_ < int(years):
                ptl_[n_, y_] += 1
        pt_out = dict(place_turnover=list(getattr(WL.W, "pt_log", None) or []), pt_lives=ptl_)
    return dict(world=wout, **(dict(grey_y=np.stack(grey_y, 1)) if GG_ON and grey_y else {}), w=softmax(z), z=z, k=k, y=y, a=softmax(y), gates=gates, M=M, J=J, sig=sig, need=need, chan=chan, conv=conv_log,
                rites=rite_log, W_hist=np.array(W_hist), M_hist=np.array(M_hist), S_hist=np.array(S_hist),
                events=events, nic=nic, D=D, stage=stage, A_hist=np.array(A_hist),
                R_hist=np.array(R_hist), K_hist=np.array(K_hist), commits=commit_log, **({"births": birth_log} if (P["birth_free"] or P["birth_par"] is not None) else {}),
                V_hist={k_: np.array(v_) for k_, v_ in V_hist.items()}, A_src=np.array(A_src), breaks=brk_log, Q=Q, history=hist, outside=ev_log,
                clashes=clash_log + [(int(n), int(kk), int(clash0[n, kk]), T, "still living with it", round(float(clashI[n, kk]), 2), int(np.argmax(softmax(z[n]))))
                                     for n, kk in zip(*np.nonzero(clash0 >= 0))], held=held, I=I, prof=prof, res=res, tries=tries, wins=wins, blocked=blocked,
                sit_n=sit_n, sit_names=L["names"], life_events=lev_log, rebounds=reb,
                goals=goal_log, goal_state=dict(kind=gk, mix=gm, domain=gd, strength=gs, progress=gp, valued=gv, harmonious=ga,
                                                invested=gi, born=gb, due=gh, horizon=ghz, source=gsrc, trigger=gtrig, felt=gfelt,
                                                chance=gch, p_step=gph, by_player=gby, id=gid, aims=gtt,
                                                lost=dict(mix=lost_m, domain=lost_d, strength=lost_s, age=lost_t, on=lost_on, id=lost_id)),
                regret=regret, marks=dict(names=L["MARKS"], n=mark_n, last=mark_last, ok=mark_ok, log=mark_log), alive=alive, **(dict(returns=ep_seeds) if EP_ON else {}), **(dict(bold=bold_log) if BO_ON else {}),
                read_log=read_log, read_names=[e_["name"] for e_ in EVR], widowed=widowed, seasons=sea_log,
                identity=dict(female=female, attr=attr, unease=unease, gender_self=gender_self, intersex=intersex, ace=ace,
                              **(dict(named=named_g, came_out=came_o, partner_same=partner_same, role_fit=1 - rfit_avg,
                                      cross_title=cross_title, role_strict=RS0, accept_trans=AT0,
                                      found={k_: found_id[:, i_] for i_, k_ in enumerate(("gender", "attraction", "ace", "intersex"))})
                                 if ID2 else {})), died=died,
                cond_hold=cond_hold.sum(0) / max(cond_n.sum(), 1), drv_mean=drv_sum / np.maximum(drv_cnt, 1),
                chance_ref=dict(ref=ref_sum / np.maximum(ref_cnt, 1)[:, None], n=ref_cnt, earn=earn_sum / np.maximum(earn_cnt, 1),
                                earn_n=earn_cnt, p_option=pk_sum / np.maximum(pk_cnt, 1), n_option=pk_cnt),
                roles=(dict(names=GR["names"], kinds=GR["kindname"], NT=NT_, has=r_has, ever=r_ever, since=r_since, end=r_end,
                            access=p_acc, level=p_lev, log=role_log, profile=r_prof, pwords=GR["pwords"], refines=GR["refines"])
                       if RON else None),
                adjectives=dict(names=ADJ_NAMES[:NA_OUT], say=ADJ_SAY[:NA_OUT], has=adj[:, :NA_OUT], since=adj_since[:, :NA_OUT],
                                log=adj_log),   # with shadows off, without the shadow states (never held then)
                **(dict(asked=asked) if CU_ON else {}),
                **(dict(btrust=btrust.copy(), btrust_y=bt_y) if BT_ON else {}),
                **(dict(prison_ties=pt_log) if P.get("prison_ties") else {}),   # part 4: ties made and ended (switch on only)
                **(dict(current=cur_sum) if CUR_ON else {}),
                **(dict(body=dict(body=body_v, mind=mind_v, conditions=dict(weight=bd_cw, kind=bd_ck, age=bd_ca, kinds=COND_KINDS),
                                  serious=dict(kind=bd_sk, since=bd_s0, until=bd_s1, kinds=SER_KINDS), kept=bd_keep,
                                  constitution=bd_con, resilience=md_res, threats=md_end, decline=dict(at=dl_at, since=dl_t0, cause=list(dl_cause))))
                   if HM_ON or DTH_ON else {}),
                **(dict(need_map=dict(person=NMP, shared=NMAP, needs=list(NEEDS))) if NM_ON else {}),
                **(dict(shadows=dict(states=SH_STATES, part=shS, force=shA, sources=sh_src, seen=sh_seen, last_seen=sh_rt,
                                     shown=sh_n, log=sh_log)) if SHON else {}),
                **(dict(areas=dict(names=AREAS, offsets=Dz, hist=D_hist,   # each area's colors are softmax(core z + offset)
                                   colors=softmax(z[:, None, :] + Dz, -1))) if DOM_ON else {}), **pt_out,
                **(dict(aims=dict(names=AIM["names"], log=aim_log, aim=ak, strength=astr, steps=astep, own=aown, by_player=aby,
                                  calling=acall, best=aim_best, goal_aim=gal, missing=AIM["missing"])) if AIM_ON else {}),
                **(dict(heights=dict(names=list(AIM_HEIGHTS), week=ht_t)) if HT_ON else {}))
