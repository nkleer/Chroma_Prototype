# run_17_inner.py: part 17 of 18 of engine._run, the life loop.
# 4b2 to 4e. felt horizon, temperament, dreams and plans, peace, upkeep, identity and own death.
# Lines here are _run's own, unchanged and at their own indent: engine.py joins the parts in order (engine.RUN_PARTS)
# and compiles them as one, so a name used here may be set in an earlier part. Never import or run it alone.
        # ---- 4b2. v7 felt horizon: years a person feels are left (age, health), shortened by reminders of mortality
        if P["hz_k"] or P["hz_want"]:
            hea_ = res[:, HEA]
            hz_mem += P["hz_remind"] * _uclip((hea_last - hea_ - 0.05) / 0.2, 0, 1) * (hea_last >= 0)   # a health shock
            hea_last = hea_.copy()
            hz_mem *= 0.5 ** (1 / (52 * P["hz_mem_half"]))
            yl_ = np.maximum(P["hz_life"] - age, 1.0) * _uclip(hea_ / P["hz_health"], 0.2, 1.0)
            ltd_ = _uclip(1 - yl_ / P["hz_span"] + hz_mem, 0, 1)
            fhz += (ltd_ - fhz) / (52 * P["hz_lag"])

        # ---- 4c. temperament (v5): four slow traits learned from the life lived, fastest in childhood
        if TON:
            lrT = P["T_rate"] * TST[stage]
            # reactivity follows how harsh (stress), unpredictable (surprise) and supportive (safety, belonging) life has been
            sup = need[:, :2].mean(1)
            r_now = _uclip(1 + P["r_harsh"] * (stress - RR[0]) + P["r_unpred"] * np.where(idle, 0.0, np.abs(delta) / stakes - RR[1])
                            - P["r_support"] * (sup - RR[2]), 0.3, 2.5)
            react += (lrT if RST is None else P["T_rate"] * RST[stage]) * (r_now - react)
            # steadiness: succeeding in what one holds confirms who one is; failing in it shakes that; roles and being
            # who one wants to be steady a person; everything fades slowly
            own = np.maximum(0, 5 * (ma * hold).sum(1) - 1) * (~idle)
            steady += (stakes * own * np.where(succ, P["s_conf"], -P["s_hit"]) + P["s_role"] * (held * I).sum(1)
                       + P["s_fit"] * np.maximum(0, 0.15 - gap) - P["s_decay"] * steady)
            steady = np.maximum(steady, 0)
            # baseline mood: a slow average of how content life has been
            base_mood += lrT * (content - base_mood)
            # outlook: did trying work? Blocked or failed wanting teaches helplessness, success teaches control
            ev_o = has & (tried | lost_open)
            outlook += np.where(ev_o, 4 * lrT * stakes * (np.where(tried & succ, 1.0, 0.0) - outlook), 0.0)
            outlook = _uclip(outlook, 0, 1)

        # ---- 4d. v7 dreams, passions and plans: new ones, fading, letting go, deadlines, regret
        if GON:
            a_now_ = softmax(y); own_g = 0.5 * (w + a_now_)
            # sparks (1A): someone or something the person admires (a parent at work, a teacher, a book, a film, a parade)
            # starts a dream when what it shows speaks to who they are and want to be
            for n in np.nonzero(rng.random(N) < np.asarray(P["dream_rate"])[stage] / 52 * (age >= 4))[0]:
                st = stage[n]
                ex_src = np.array([0.5 + res[n, TIE], 0.5 + 0.5 * turn_pm[n], 0.3 + 0.5 * res[n, MON] + 0.5 * res[n, FRE],
                                   0.5 + 0.5 * held[n, COM] + e_i, 0.5 + 0.5 * turn_pm[n]])
                wt = TRIG_W[:, st] * ex_src[TRIG_SRC]
                if DG_ON:   # F6: a spark comes only at the ages its telling fits (a school visit, the elders' teaching)
                    wt = wt * ((TRIG_AGE[:, 0] <= age) & (age <= TRIG_AGE[:, 1]))
                if wt.sum() <= 0:
                    continue
                tr = int(rng.choice(len(wt), p=wt / wt.sum())); sc = TRIG_SRC[tr]
                wp_ = np.asarray(P["world_profile"], float)
                culture = 0.5 * wp_ / wp_.sum() + 0.5 * (e_p if e_i > 0 else np.full(C, 0.2))
                if sc == 0:
                    msg = rng.dirichlet(20 * fam[n] + 0.1)
                elif sc == 1:
                    msg = rng.dirichlet(20 * circle[n] + 0.1)
                elif sc == 2:
                    msg = random_messages(rng, 1)[0] if rng.random() < 0.6 else rng.dirichlet(20 * culture)
                elif sc == 3:
                    msg = rng.dirichlet(20 * culture) if rng.random() < 0.6 else random_messages(rng, 1)[0]
                else:
                    msg = random_messages(rng, 1)[0]
                if TRIG_TILT[tr].sum() > 0:
                    msg = 0.5 * msg + 0.5 * TRIG_TILT[tr] / TRIG_TILT[tr].sum()
                lens = 0.5 * softmax(k[n]) + 0.5 * a_now_[n]
                adm = 1 / (1 + np.exp(-(P["d_adm0"] + P["d_fit"] * (5 * (lens * msg).sum() - 1) + P["d_open"] * min(B[n], 2) / 2)))
                if rng.random() >= adm:
                    continue
                g_ = np.maximum(msg * (1 + P["d_read"] * (5 * lens - 1)), 0)      # read through their own colors
                g_ = 0.8 * g_ / max(g_.sum(), 1e-9) + 0.2 * lens
                subj_ = -1
                if DG_ON and TRIG_SUBJ[tr]:   # F6: the spark keeps its subject: of the dreams it shows, the one nearest their
                    dgc_ = [i_ for i_ in TRIG_SUBJ[tr] if DRM_FROM[i_] <= age and DRM_S[i_, st]   # colours that they are old
                           and not (st >= 2 and DRM_D[i_] >= 0 and held[n, DRM_D[i_]])]           # enough for and do not hold
                    if not dgc_:
                        continue                                                 # too young for any of them: no dream yet
                    subj_ = dgc_[int(np.argmax(DRM_M[dgc_] @ (g_ - 1 / C)))]
                    g_ = (1 - P["dream_subj"]) * g_ + P["dream_subj"] * DRM_X[subj_]   # its ways, partly the subject's
                dw = np.asarray(P["d_dom"], float).copy()
                fitd = KPAY @ (NMAP @ g_); dw[:NK] *= fitd / fitd.mean()        # what the dream is about follows what its ways serve
                if st >= 2:
                    dw[:NK] *= ~held[n]
                if SEEN_ON and SD_AGES_[0] <= age <= SD_AGES_[1]:   # S6: from 8 to 20 a dream is about a path they have seen
                    dw[:NK] *= 1 + SD_DREAM_ * WL.PP.seen_dom(n)    # more often (the sparks' rate as it was)
                if DG_ON and subj_ < 0:   # F6: only what a dream of their age can be about
                    dgf_ = (DRM_FROM <= age) & DRM_S[:, st]
                    dgh_ = np.array([(dgf_ & (DRM_D == d_)).any() for d_ in range(NK)] + [(dgf_ & (DRM_D < 0)).any()])
                    if (dw * dgh_).sum() > 0:
                        dw = dw * dgh_
                if subj_ >= 0:
                    dom = int(DRM_D[subj_])
                else:
                    dom = int(rng.choice(NK + 1, p=dw / dw.sum())); dom = dom if dom < NK else -1
                new_goal(n, 0, g_, dom, sc, trig=tr, s0=0.2 + 0.4 * adm, name=subj_)
                if SEEN_ON and n in events and SD_AGES_[0] <= age <= SD_AGES_[1]:   # S6: a dream seeded from a seen path
                    sd_ = WL.PP.seen_dream(n, dom)                                    # and its model (the Library's "dream")
                    if sd_:
                        events[n].append(dict(seen=dict(sd_, age=round(age, 2))))
            # fading: an unfed dream fades (fast in childhood); a passion only when unpractised for a year; a plan that
            # does not fit who one is loses its pull (self-concordance: Sheldon & Elliot 1999)
            fd_ = np.exp(-np.log(2) / (52 * np.asarray(P["d_half"], float)[stage]))[:, None]
            if DG_ON:   # F6: a young child's play dream is short-lived (children of 4 to 8 change them often)
                fd_ = np.where(gplay, np.exp(-np.log(2) / (52 * P["dream_play_half"])), fd_)
            gs = np.where(gk == 0, gs * fd_, gs); gv = np.where(gk == 0, gv * fd_, gv)
            gs = np.where((gk == 1) & (t - glast > 52), gs * np.exp(-np.log(2) / (52 * P["pass_half"])), gs)
            conc_g = _uclip(2 * np.einsum("ngc,nc->ng", gm, own_g) / own_g.max(1)[:, None] - 1, -0.5, 1)
            gs = np.where((gk == 2) & (gby == 0), gs - P["g_decay"] * (1 - np.maximum(conc_g, 0)) * gs, gs)
            # an obsessive passion gnaws when the person is kept from it (rumination)
            stress = stress + P["op_rum"] * (((gk == 1) & (t - glast > P["op_away"])) * gs * (1 - ga)).sum(1)
            # a turning point seals a dream as a rite does: a big life event met in the dream's ways, and it worked
            if P["base_rates"]:
                for n in np.nonzero(big & succ)[0]:
                    seal(n, "a turning point", only=set(np.nonzero((gk[n] == 0) & (ra[n] >= 0.5))[0].tolist()))
            for n, j in zip(*np.nonzero((gk >= 0) & (gs < 0.08) & (gby == 0))):
                end_goal(n, j, ("faded", "faded", "drifted away")[gk[n, j]])
            # new plans (adults; a plan is not a commitment): a resolution at a birthday, a passion that wants room,
            # an unmet need, an old dream that returns
            npl = (gk == 2).sum(1); room_ = (npl < P["max_plans"]) & (stage >= 2)
            if t % 52 == 0:   # fresh start (Dai, Milkman & Riis 2014): birthdays invite resolutions
                gap_now = 0.5 * np.abs(a_now_ - w).sum(1)
                for n in np.nonzero(room_ & (rng.random(N) < P["res_p"] * _uclip(gap_now / 0.15, 0, 2)))[0]:
                    pos_ = np.maximum(a_now_[n] - w[n], 0)
                    if new_goal(n, 2, 0.5 * a_now_[n] + 0.5 * pos_ / max(pos_.sum(), 1e-9), -1, GSRC["resolution"], hz=1, s0=0.35) >= 0:
                        npl[n] += 1
            room_ = (npl < P["max_plans"]) & (stage >= 2)
            kid_ = np.zeros((N, NGS), bool)
            for j in range(NGS):
                kid_[:, j] = ((gpar == j) & (gk == 2)).any(1)
            cand = (gk == 1) & ~kid_ & room_[:, None] & (rng.random((N, NGS)) < P["pass_plan"] / 52 * gs)
            for n, j in zip(*np.nonzero(cand)):
                if npl[n] >= P["max_plans"]:
                    continue
                d_ = gd[n, j]
                if d_ >= 0 and (held[n, d_] or (d_ == CAR and (retired[n] or age > 60)) or (d_ == KID and age > 45)):
                    d_ = -1
                hz = 3 if (d_ < 0 and rng.random() < 0.3) else 2
                if new_goal(n, 2, gm[n, j].copy(), d_, GSRC["passion"], hz=hz, par=j, s0=0.3 + 0.4 * gs[n, j]) >= 0:
                    npl[n] += 1
            room_ = (npl < P["max_plans"]) & (stage >= 2)
            desire = (nimp * np.maximum(0, P["need_set"] - need) / P["need_set"]) @ KPAY.T            # N,NK
            elig = ~held & room_[:, None]
            elig[:, CAR] &= ~retired & (age < 60); elig[:, KID] &= (age < 45)
            for d_ in range(NK):
                elig[:, d_] &= ~((gk == 2) & (gd == d_)).any(1)
            pdom = P["dom_plan"] / 52 * desire * elig * np.where(np.arange(NK) == KID, 0.3 + 0.7 * held[:, PAR][:, None], 1.0)
            hit_d = rng.random((N, NK)) < pdom
            for n in np.nonzero(hit_d.any(1))[0]:
                d_ = int(np.argmax(np.where(hit_d[n], pdom[n], -1)))
                if new_goal(n, 2, 0.5 * a_now_[n] + 0.5 * w[n], d_, GSRC["need"], hz=2, s0=0.3 + 0.4 * min(1.0, desire[n, d_])) >= 0:
                    npl[n] += 1
            room_ = (npl < P["max_plans"]) & (stage >= 2)
            fit_l = _uclip(5 * (lost_m * a_now_[:, None, :]).sum(2) - 1, 0, 2) / 2
            p_rv = (P["revive"] / 52 * fit_l * lost_s * lost_on * room_[:, None]
                    * (res[:, FRE] * (0.5 + res[:, TIM]) * (1 + 2 * regret))[:, None])
            for n, q_ in zip(*np.nonzero(rng.random((N, 3)) < p_rv)):
                if npl[n] >= P["max_plans"]:
                    continue
                d_ = lost_d[n, q_]
                if d_ >= 0 and (held[n, d_] or (d_ == CAR and (retired[n] or age > 60)) or (d_ == KID and age > 45)):
                    d_ = -1
                if new_goal(n, 2, lost_m[n, q_].copy(), d_, GSRC["old dream"], hz=2, s0=0.4, name=lost_nm[n, q_]) >= 0:
                    lost_on[n, q_] = False; npl[n] += 1
            # felt odds, letting go and deadlines
            pln = gk == 2
            if pln.any():
                wl = np.minimum(gh - t, max(52.0, (P["life_end"] - age) * 52))
                steps = np.ceil((1 - gp) * np.asarray(P["g_size"], float)[ghz] / STEP_INC).astype(int)
                fo_ = np.nonzero(pln)   # speed pass: the felt odds of the plans alone (each plan's odds is its own; the rest went unused)
                gfelt = gfelt.copy(); gfelt[fo_] = felt_odds(gch[fo_], gph[fo_], wl[fo_], steps[fo_], gd[fo_],
                                                             np.broadcast_to(outlook[:, None], pln.shape)[fo_], P)
                # clinging to a plan that seems hopeless is stressful (Wrosch et al. 2003)
                stress = stress + P["g_ruminate"] * (pln * gs * _uclip((0.3 - gfelt) / 0.3, 0, 1)).sum(1)
                fa_ = _uclip((tries - wins + blocked - P["flex_exp"][0]) / P["flex_exp"][1], 0, 1)
                letgo = 0.3 + 0.7 * fa_               # having seen wanted things fail makes letting go easier
                sunk = 1 - np.exp(-gi)                 # what has been put in holds people to a plan
                drop = (pln & (gby == 0) & (gfelt < P["g_drop"]) & (rng.random((N, NGS)) < 1 / 13)
                        & (rng.random((N, NGS)) < letgo[:, None] * (1 - sunk)))
                for n, j in zip(*np.nonzero(drop)):
                    quit_(n, j, "let go", letgo[n])
                for n, j in zip(*np.nonzero((gk == 2) & (t >= gh))):
                    hw = HORIZON_W[ghz[n, j]]
                    if hw is not None and hw > 1 and gx[n, j] < 2 and gby[n, j] == 0:
                        felt2 = float(felt_odds(gch[n, j], gph[n, j], hw, steps[n, j], gd[n, j], outlook[n], P))
                        p_ext = 1 / (1 + np.exp(-(3 * (felt2 - 0.35) + 1.5 * sunk[n, j] + (gsrc[n, j] == GSRC["passion"]) - 1.5 * letgo[n])))
                        if rng.random() < p_ext:   # more time, the same plan (sunk cost, and the planning fallacy again)
                            gh[n, j] = t + hw; gx[n, j] += 1; glog(n, j, "extended")
                            continue
                    quit_(n, j, "not reached in time", letgo[n])
            if t % 52 == 0:   # regret of what was let go grows over a decade when it still fits (Gilovich & Medvec 1995)
                yrs_ = _uclip((age - lost_t) / 10, 0, 1)
                regret = (lost_on * lost_s * _uclip(5 * (lost_m * a_now_[:, None, :]).sum(2) - 1, 0, 1) * yrs_).sum(1) / 3

        # coherence under the world's framing, softened by what this person has integrated
        Tm = np.maximum(FR, 0)[None] * (1 - J) + np.minimum(FR, 0)[None]
        G = np.einsum("nij,nj->ni", Tm, w)
        tension = np.einsum("ni,nij,nj->n", w, np.maximum(FR, 0)[None] * (1 - J), w)   # opposed colors held at once
        # peace (meta variable): the absence of agitation. Stress, ought conflict with commitments, inner tension
        # between colors the world frames as opposed, and blocked wanting all disturb it
        q_thr = P["q_theta"] * np.maximum(hold_against, 0.2) ** P["q_hold"]
        q_rel = Q / q_thr
        p_now = 1 / (1 + np.exp(-(P["pc_mid"] - P["pc_stress"] * stress - P["pc_clash"] * cload
                                  - P["pc_tension"] * tension - P["pc_pent"] * q_rel)))
        peace += (p_now - peace) / P["meta_weeks"]
        if P["adjectives"] and t % 4 == 0:   # v7 adjectives: each month, with a margin so a state does not flicker
            src_ = dict(content=content, peace=peace, mood=mood, stress=stress, wound=wound, discipline=dsc, gap=gap_r,
                        unmet_hope=hzf * np.maximum(unmet, 0), **{"shadow_" + c_: shA[:, i_] for i_, c_ in enumerate(COLORS)})
            src_.update({nm_: need[:, i_] for i_, nm_ in enumerate(NEEDS)}); src_.update({nm_: res[:, i_] for i_, nm_ in enumerate(RESOURCES)})
            av_ = np.stack([np.broadcast_to(src_[a_[2]], (N,)) for a_ in ADJ_ALL], 1) * ADJ_SIDE
            adj_v = av_ if adj_v is None else adj_v + P["adj_smooth"] * (av_ - adj_v)    # the last few months
            old_ = adj
            adj = ((adj_v >= ADJ_ON * ADJ_SIDE) | (adj & (adj_v >= ADJ_OFF * ADJ_SIDE))) & (age >= ADJ_AGE)
            for n, a_ in zip(*np.nonzero(adj != old_)):
                what_ = "gained" if adj[n, a_] else "lost"
                adj_log.append((int(n), t, int(a_), what_))
                if adj[n, a_]:
                    adj_since[n, a_] = t
                if n in events:
                    events[n].append(dict(adj=dict(age=round(age, 2), name=ADJ_NAMES[a_], say=ADJ_SAY[a_], what=what_)))
        dC = -MU_ * w * (G - (w * G).sum(1, keepdims=True))
        J += P["iota"] * np.maximum(delta, 0)[:, None, None] * \
            np.einsum("ni,nj->nij", ma, ma) * 4 * (1 - J) * (1 - np.eye(C))[None]
        if P["ten_bad"]:   # v6: a failed attempt to hold both loosens what had been integrated
            J -= P["iota"] * P["ten_split"] * np.maximum(-delta, 0)[:, None, None] * np.einsum("ni,nj->nij", ma, ma) * 4 * J * (1 - np.eye(C))[None]

        # upkeep: a concentrated identity decays toward balance unless constantly fed
        conc = ((w ** 2).sum(1) - 0.2) / 0.8
        # shadows replace the flat upkeep: an active shadow pulls its own color back (its costs teach), the rest share it
        if not SHON:
            dU = -P["upkeep"] * conc[:, None] * z
        elif P["sh_form"] == "balance":   # back toward what the person lacks, as strongly as their strongest shadow
            dU = -P["sh_pull"] * shA.max(1)[:, None] * z
        else:                             # "own": the shadowed color itself gives way
            dU = -P["sh_pull"] * shA * np.maximum(z, 0)
            if P["sh_will"]:   # sh_will: less on a colour wanted beyond what is held
                dU = dU * (1 - P["sh_will"] * _uclip(5 * (softmax(y) - w), 0, 1))

        # ---- 4e. identity and the character's own death (point 11)
        if t % 52 == 0 and age >= 25 and P["attr_drift"]:   # a woman's attraction can shift a step in adult life
            dr_ = female & (attr != 2) & ((idr_ if ID2 else rid).random(N) < P["attr_drift"])
            attr[dr_] += np.where(attr[dr_] < 2, 1, -1)
        if ID2 and BAT:   # N1b (chroma-identity/for-the-engine.md)
            newp_ = held[:, PAR] & ~par_prev                 # a new partner: of the same sex or not, by attraction (Pew 2013)
            for n in np.nonzero(newp_)[0]:
                partner_same[n] = ps_u[n, min(ps_n[n], ps_u.shape[1] - 1)] < PSP_[attr[n]]; ps_n[n] += 1
            partner_same &= held[:, PAR]; par_prev = held[:, PAR].copy()
            if IDF_ON:   # found: the first week a moment about a trait the person has comes (the game shows it from then)
                hv_ = np.stack([gender_self > 0, attr >= 1, ace, intersex], 1)
                fd_ = IDG[s] & hv_ & (found_id <= NEVER // 2) & ~dead[:, None]
                if fd_.any():
                    found_id[fd_] = t
                    for n in set(np.nonzero(fd_.any(1))[0].tolist()) & set(events):
                        for k_ in np.nonzero(fd_[n])[0]:
                            events[n].append(dict(found=dict(age=round(age, 2), trait=("gender", "attraction", "ace", "intersex")[k_])))
            rs_w, at_w, ex_w = role_view()
            cwt_ = np.zeros(N)
            if TROLE_ON:   # a title the world reserves for the other sex, as they are expected: a small weekly strain
                th_ = r_has[:, :NT_] & (TROLE_ >= 0)[None]
                if th_.any():
                    cwt_ = np.where(th_, ex_w[:, 1 - _uclip(TROLE_, 0, 1)], 0.0).max(1)
                    stress += P["role_title_stress"] * rs_w * cwt_ * ~dead
            cross_title = cwt_ >= 0.5
            hidg_ = (gender_self > 0) & ~named_g & (age >= P["aware_age"])
            x_ = np.maximum(np.maximum(act_cw, cwt_), hidg_.astype(float))
            rfit_avg += (1 - 0.5 ** (1 / (52 * P["role_fit_hl"]))) * (x_ - rfit_avg)
        if BAT and P["hide_stress"] and age >= P["aware_age"] and ID2:   # hiding each trait weighs on them until they tell it;
            # gender more where it is less accepted; after telling, a share stays where the world is hostile (Meyer 2003)
            clim_ = P["climate"] + (clim_w if WON else 0.5 * faith_given * I[:, FAI])   # the world: local norm and the right
            o_ = (attr >= 2) & ~dead; g_ = (gender_self > 0) & ~dead
            ho_ = (1 + clim_) * np.where(came_o, P["out_stress"] * clim_, 1.0) * o_
            hg_ = (1 + clim_) * (1.5 - at_w) * np.where(named_g, P["out_stress"] * (1 - at_w), 1.0) * g_
            stress += P["hide_stress"] * (ho_ + hg_)
        elif BAT and P["hide_stress"] and age >= P["aware_age"]:   # hiding who they are weighs on them until they come out
            came_ = mark_n[:, MIDX["came out"]] > 0 if "came out" in MIDX else np.zeros(N, bool)
            hid_ = ((attr >= 2) | unease) & ~came_ & ~dead
            if hid_.any():
                stress += P["hide_stress"] * hid_ * (1 + P["climate"] + (clim_w if WON else 0.5 * faith_given * I[:, FAI]))
        if P["self_death"] and DTH_ON:   # v22.5 F2: death from the life
            death_week()
        elif P["self_death"]:   # the life table, likelier in poor health
            sm_ = P["self_mort"]
            q_ = np.minimum(1, (sm_[0] + sm_[1] * np.exp(sm_[2] * age)) * np.exp(P["self_health"] * (0.6 - res[:, HEA])))
            for n in np.nonzero(~dead & (rid.random(N) < q_ / 52))[0]:
                die(n, "illness" if age < 75 else "old age")
        if RON and (pris_out == t).any():   # out of prison
            for n in np.nonzero(pris_out == t)[0]:
                if "ex-prisoner" in GR["ID"]:
                    r_gain(n, GR["ID"]["ex-prisoner"], "released")
        if PT_TEST is not None and t == int(round(52 * PT_TEST[0])):   # part 4's checks: every living life starts a term
            pris_in = np.where(dead, pris_in, t); pris_out = np.where(dead, pris_out, t + int(round(52 * PT_TEST[1])))
        if EXP_I >= 0:   # part 4: this week's releases: a known term's end, or [ex-prisoner] by its rule with no term pending
            rk_ = pris_out == t
            rr_ = r_has[:, EXP_I] & (r_since[:, EXP_I] != pt_seen) & ~rk_ & ~(pris_out > t)
            pt_seen = np.where(r_has[:, EXP_I], r_since[:, EXP_I], pt_seen)
            rel_ = (rk_ | rr_) & ~dead
            if rel_.any():
                pt_rel = np.where(rel_, t, pt_rel)
                if PT_ON:
                    pt_release(np.nonzero(rel_)[0], rk_[rel_])
        if PT_ON:   # the ties still active; the pull back while their lead colour's shadow part is over .5 (shadow) and they hold
            pt_week()   # neither a partner nor steady work (a job a year or more: Sampson and Laub 1993)
            sw_ = (r_has[:, PT_JOB] & (t - r_since[:, PT_JOB] >= 52)).any(1) if len(PT_JOB) else np.zeros(N, bool)
            pt_pull = (pt_pull_of(pt_act, shS[ar, np.argmax(w, 1)], PTP_["shadow"], held[:, PAR], sw_) if SHON
                       else np.zeros(N, bool))
            if t % 4 == 0:   # shared understanding: stress -.01 a month in the first year out
                stress += PT_STM * (pt_act & (t - pt_rel < 52) & (pt_rel > NEVER))

