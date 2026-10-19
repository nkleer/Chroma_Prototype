# run_14_marks.py: part 14 of 18 of engine._run, the life loop.
# 3d. what the week leaves: the act's titles, deaths, endings, marks, moves, tags, backfire, work again.
# Lines here are _run's own, unchanged and at their own indent: engine.py joins the parts in order (engine.RUN_PARTS)
# and compiles them as one, so a name used here may be set in an earlier part. Never import or run it alone.
        if BAT:
            # ---- 3d. the Library's batch: what this week leaves in the person's history
            live_ = ~recon
            sit_last[ar[live_], s[live_]] = t
            fs_ = sit_first[ar[live_], s[live_]] <= NEVER // 2
            sit_first[ar[live_][fs_], s[live_][fs_]] = t
            on_ = ONCE[s] & live_
            once_done[ar[on_], ROOT[s[on_]]] = True       # a child version and its original are one event (variant_of)
            if RON:   # the act's titles and perks: becoming a nurse, a licence taken (on success; the _if_fails fields on failure)
                for n in np.nonzero(GR["A_HASFX"][s, a] & ~idle & live_ & (bold_pick < 0))[0]:
                    for op_, j0_, yrs_ in GR["A_FX"][(int(s[n]), int(a[n]))]["ok" if succ[n] else "fail"]:
                        if j0_ == LONG_ and not succ[n]:
                            continue                           # [a long shot that missed]: only after a real long shot, below
                        for j_ in fx_targets(n, int(s[n]), j0_):
                            r_act(n, op_, j_, yrs_, "through " + L["labels"][s[n]][a[n]], ma[n])
                if BO_ON:   # a bold pick: the bold way's act fields in place of its base way's (the first one named is the
                    for n in np.nonzero((bold_pick >= 0) & ~idle & live_)[0]:   # title its links tell of)
                        bor_ = BO_ROWS[bo_row[n, bold_pick[n]]]; bo_title[n] = None
                        for op_, j0_, yrs_ in bor_["fx"]["ok" if succ[n] else "fail"]:
                            if j0_ == LONG_ and not succ[n]:
                                continue
                            for j_ in fx_targets(n, int(s[n]), j0_):
                                bo_title[n] = GR["names"][j_] if bo_title[n] is None else bo_title[n]
                                r_act(n, op_, j_, yrs_, "through " + bor_["label"], ma[n])
                if C5F_ >= 0 and WL is not None:   # C5: "a following of your own" taken and working founds the movement in
                    # their town: its colours become the founder's own, its growth scales with their reach (ties .8 is 1)
                    for n in np.nonzero((GR["A_TITLE"][s, a] == C5F_) & succ & ~idle & live_)[0]:
                        WL.W.c5_found_by(np.asarray(w[n], float)[WL.W.perm], reach=float(res[n, TIE]) / 0.8)
                at_l = missed_at(GR["A_TITLE"][s, a], s, a)    # a failed try for a title at true odds under long_shot: a long shot
                for n in np.nonzero(long_miss)[0]:              # that missed, whatever the option names (election night with no
                    if at_l[n] >= 0:                          # nomination, the part of a lifetime for an unknown); packs 08:02
                        missed_t[n] = at_l[n]
                    if LONG_ >= 0:
                        r_gain(n, LONG_, "through " + L["labels"][s[n]][a[n]] + (" (missed: " + GR["names"][at_l[n]] + ")"
                                                                                 if at_l[n] >= 0 else ""), ma[n])
                for n in np.nonzero(GR["S_HASFX"][s] & live_)[0]:   # the moment itself gives it (going into foster care)
                    for op_, j0_, yrs_ in GR["S_FX"][int(s[n])]:
                        for j_ in fx_targets(n, int(s[n]), j0_):
                            r_act(n, op_, j_, yrs_, "through " + L["names"][s[n]], None)
                for n in np.nonzero(RETIRES_[s] & live_ & held[:, CAR])[0]:   # the last day at work: the career ends here
                    end([n], [CAR], "retired", t); ret_pend[n] = -1
                if AD_ON:   # a risky act that fails can end the life (never a child's own act); with self_death off it
                    # leaves the body badly hurt instead
                    # a failure that does not kill can still put the person in hospital: near_ratio times as often as death
                    # (non-fatal overdoses and crash injuries far outnumber deaths); with self_death off, deaths are near
                    # misses too
                    for n in np.nonzero((A_DEATH[s, a] > 0) & ~succ & ~idle & live_ & (age >= 13))[0]:
                        u_ = rid.random(); sh_ = A_DEATH[s[n], a[n]]
                        if u_ < sh_ and P["self_death"]:
                            die(n, "through " + L["labels"][s[n]][a[n]])
                        elif u_ < min(1.0, P["near_ratio"] * sh_):
                            res[n, HEA] = max(0.0, res[n, HEA] - 0.3); stress[n] += 0.5; ago["near_death"][n] = t
                            if n in events:
                                events[n].append(dict(near_death=dict(age=round(age, 2), through=L["labels"][s[n]][a[n]])))
                if AK_ON:   # taking a life (by choice, rarely; never a child's act, never a child): the person is gone,
                    # [has taken a life], and about half are caught: a record, the job lost, prison, then [ex-prisoner]
                    for n in np.nonzero((A_KILL[s, a] != -1) & succ & ~idle & live_ & (age >= 13))[0]:
                        r_ = int(A_KILL[s[n], a[n]])
                        if r_ >= 0 and ROLES[r_] == "partner":
                            if held[n, PAR]:
                                end([n], [PAR], "widowed", t)
                        elif r_ >= 0 and WON:   # the world's cast: that person is gone
                            WL.PP.kill(int(n), ROLES[r_]); alive[n, :5] = WL.PP.alive[n]
                        elif r_ >= 0:
                            alive[n, r_] = max(alive[n, r_] - 1, 0)
                        stress[n] += 1.0; ago["death"][n] = t; ago["loss"][n] = t
                        caught_ = bool(rid.random() < P["kill_caught"])
                        if "has taken a life" in GR["ID"]:
                            r_gain(n, GR["ID"]["has taken a life"], "took a life")
                        if caught_ and EYES_ON_:   # S3: a crime found out, read by their places in the act's colours
                            WL.PP.eyes_see([n], ma[n][None], [0.0], "crime")
                        if caught_ and BT_ON:   # body_trust: an arrest and a verdict, a run-in gone against them
                            for j_ in (BT_PROT_J, BT_RULE_J):
                                WL.PP.bt_jump(n, j_, BTJ_["own_run_in_bad"], "bad")
                        if caught_:
                            if "someone with a record" in GR["ID"]:
                                r_gain(n, GR["ID"]["someone with a record"], "arrested")
                            if held[n, CAR]:
                                end([n], [CAR], "lost job", t)
                            pris_out[n] = t + int(52 * rid.uniform(*P["kill_prison"]))
                            pris_in[n] = t
                        if n in events:
                            events[n].append(dict(killed=dict(age=round(age, 2), role=ROLES[r_] if r_ >= 0 else "someone",
                                                              through=L["labels"][s[n]][a[n]], caught=caught_)))
                if AKF_ON:   # an act that fails costs someone their life (an overdose nobody stopped): grief, not a crime
                    for n in np.nonzero((A_KILLF[s, a] != -1) & ~succ & ~idle & live_ & (age >= 13))[0]:
                        if A_KILLFS[s[n], a[n]] < 1 and rid.random() >= A_KILLFS[s[n], a[n]]:
                            continue
                        r_ = int(A_KILLF[s[n], a[n]])
                        if r_ >= 0 and ROLES[r_] == "partner":
                            if held[n, PAR]:
                                end([n], [PAR], "widowed", t)
                        elif r_ >= 0 and WON:   # the world's cast: that person is gone
                            WL.PP.kill(int(n), ROLES[r_]); alive[n, :5] = WL.PP.alive[n]
                        elif r_ >= 0:
                            alive[n, r_] = max(alive[n, r_] - 1, 0)
                        stress[n] += 1.0; ago["death"][n] = t; ago["loss"][n] = t
                        if n in events:
                            events[n].append(dict(lost=dict(age=round(age, 2), role=ROLES[r_] if r_ >= 0 else "someone",
                                                            through=L["labels"][s[n]][a[n]])))
                if GON:   # aims: choosing it sets the person's heart on a title: a five-year plan aimed at it (pathways)
                    for n in np.nonzero((GR["A_AIM"][s, a] >= 0) & ~idle & live_)[0]:
                        x_ = int(GR["A_AIM"][s[n], a[n]])
                        if not r_has[n, x_] and not (gtt[n] == x_).any():
                            pf_ = PW_[x_, int(np.argmax(np.where(PMASK_[x_], PW_[x_] @ w[n], -np.inf)))]
                            new_goal(n, 2, pf_ if pf_.sum() > 0 else w[n].copy(), -1, GSRC["resolution"], hz=2, s0=0.6, target=x_)
            newk_ = held & ~held_wk
            for n, kk in zip(*np.nonzero(newk_)):        # a new commitment opens its once-per-commitment events again
                once_done[n, ONCE_K == kk] = False
            # deaths: someone close is gone (the partner's death also ends the partnership, below)
            for r_ in range(len(ROLES)):
                hit_ = np.nonzero((KILLS[s] == r_) & live_)[0]
                if not len(hit_):
                    continue
                hz_mem[hit_] += P["hz_remind"] * HZ_ROLE[r_]
                if ROLES[r_] == "partner":
                    widowed[hit_] = True
                elif not (WON and r_ < 5):   # with the world on, the cast counted it already (a child's is the engine's)
                    alive[hit_, r_] = np.maximum(alive[hit_, r_] - 1, 0)
                if WON and ROLES[r_] == "child":
                    for n in hit_:
                        WL.PP.kill(int(n), "child")
                if ROLES[r_] == "friend" and not WON:   # a new friend in two years (with the world on, the cast makes them)
                    friend_back[hit_] = t + int(2 * 52)
                need[hit_, NIDX["belonging"]] -= KILL_HIT[r_, 0]; stress[hit_] += KILL_HIT[r_, 1]
                ago["death"][hit_] = t; ago["loss"][hit_] = t
                for n in hit_:
                    if n in events:
                        events[n].append(dict(death=dict(age=round(age, 2), role=ROLES[r_], left=int(alive[n, r_]))))
            # endings the event brings: a breakup, a divorce, a death, a lost job
            en_ = np.nonzero((ENDS[s] >= 0) & live_ & held[ar, np.maximum(ENDS[s], 0)])[0]
            if PS_ON and len(en_):   # F9: a breakup moment ends a home together this share of the time (else a rough patch)
                en_ = en_[~(PS_SOFT[s[en_]] & (ps_rng.random(len(en_)) >= P["par_split"]))]
            for n in en_:
                kk = int(ENDS[s[n]])
                end([n], [kk], "widowed" if KILLS[s[n]] == ROLES.index("partner") else "lost job" if kk == CAR else "broke up", t)
            # marks: what the act leaves in the person's history (echoes read them years later)
            mk_ = L["MARK"][s, a]
            if BO_ON and (bold_pick >= 0).any():   # a bold pick leaves the bold way's mark: when it names one
                mk_ = mk_.copy()
                for n in np.nonzero(bold_pick >= 0)[0]:
                    mk_[n] = BO_ROWS[bo_row[n, bold_pick[n]]]["mark"] if BO_ROWS[bo_row[n, bold_pick[n]]]["mark"] >= 0 else mk_[n]
            hm_ = np.nonzero((mk_ >= 0) & ~idle & live_)[0]
            if DR_ON and len(hm_):   # F17: most acts of a rare deed pass; a share by their stakes leaves the mark
                rr_ = DR_M[mk_[hm_]]
                if rr_.any():
                    kp_ = dr_rng.random(len(hm_)) < np.minimum(1.0, P["deed_rare"] * stakes[hm_])
                    hm_ = hm_[~rr_ | kp_]
            if len(hm_):
                jj_ = mk_[hm_]; first_ = mark_n[hm_, jj_] == 0
                mark_first[hm_[first_], jj_[first_]] = t
                mark_last[hm_, jj_] = t; mark_ok[hm_, jj_] = succ[hm_]; mark_n[hm_, jj_] += 1
                heavy_risk[hm_] += (jj_ == MIDX["took a wild risk"]) & (L["BODY"][s[hm_], a[hm_]] >= 1)
                if ID2 and BAT:   # N1b: which trait a mark tells (came out in a moment about one trait tells that one)
                    for n, j_ in zip(hm_, jj_):
                        if j_ == NAMED_K or (j_ == COME_K and CO_SPLIT[s[n]] != 2):
                            if gender_self[n] > 0 and not named_g[n]:
                                named_g[n] = True
                                if j_ != NAMED_K:   # read as named their gender until the Library's marks land
                                    mark_first[n, NAMED_K] = t if mark_n[n, NAMED_K] == 0 else mark_first[n, NAMED_K]
                                    mark_last[n, NAMED_K] = t; mark_ok[n, NAMED_K] = succ[n]; mark_n[n, NAMED_K] += 1
                        if j_ == COME_K and CO_SPLIT[s[n]] != 1:
                            came_o[n] = True
                for n, j_ in zip(hm_, jj_):
                    mark_log.append((int(n), t, int(j_), bool(succ[n])))
                    if RW_ON and n in events:   # role_why: the moment and way that left the mark
                        rw_mk[(int(n), int(j_))] = (t, int(s[n]), int(a[n]))
                    if n in events:
                        events[n].append(dict(mark=dict(age=round(age, 2), mark=L["MARKS"][j_], worked=bool(succ[n]))))
            if EP_ON and P["echo_asked"]:   # picks come back: an asked pick's mark (as left) and back: plant seeds
                P["echo_asked"] = False
                left_ = set(hm_.tolist())
                for n in np.nonzero(~idle & live_)[0]:
                    nt_ = L["notes"][s[n]][a[n]] if a[n] < len(L["notes"][s[n]]) else {}
                    ks_ = [(L["MARKS"][mk_[n]], "mark")] if n in left_ else []
                    if str(nt_.get("back") or "").strip() and str(nt_["back"]).strip() not in [k_ for k_, _ in ks_]:
                        ks_.append((str(nt_["back"]).strip(), "back"))
                    for k_, src_ in ks_:
                        due_ = t + int(round(ep_rng.uniform(*EPP["delay"]) * 52)) if ep_rng.random() < EPP["p"] else None
                        ep_seeds.append(dict(n=int(n), t=t, kind=k_, src=src_, s=int(s[n]), a=int(a[n]), ok=bool(succ[n]),
                                             due=due_, done=None, got=None))
            if EP_ON and BO_ON:   # a bold pick plants its link's seed: kind bold:<moment>/<colour>, side by how it went, due
                for n in np.nonzero((bold_pick >= 0) & ~idle & live_)[0]:   # inside its links' delay:; none in a link's week
                    if ep_now[n] >= 0 and "bold" in ep_seeds[ep_now[n]]:
                        continue
                    bor_ = BO_ROWS[bo_row[n, bold_pick[n]]]; bok_b_ = bool(succ[n])
                    boch_ = bor_["change"]["well" if bok_b_ else "badly"]
                    bodl_ = [cd_["delay"] for _, _, cd_ in EP_C.get((bor_["kind"], bok_b_), ()) or EP_C.get(("change:" + boch_, bok_b_), ())]
                    bocap_ = bo_n[n] >= P["bold_cap"]   # past the cap the seed is done at once (it never comes back)
                    bolo_, bohi_ = (min(d_[0] for d_ in bodl_), max(d_[1] for d_ in bodl_)) if bodl_ else EPP["delay"]
                    bodue_ = None if bocap_ else t + int(round(ep_rng.uniform(bolo_, bohi_) * 52))
                    ep_seeds.append(dict(n=int(n), t=t, kind=bor_["kind"], src="bold", s=int(s[n]), a=int(a[n]), ok=bok_b_,
                                         due=bodue_, done=-1 if bocap_ else None, got=None, bold=int(bor_["i"]),
                                         alt="change:" + boch_ if boch_ else None, link=False, change=False, who=None, gone=False,
                                         title=bo_title[n], until=t + int(round((bohi_ + 0.25) * 52))))   # its window: delay + a season
                    bo_seed[n] = len(ep_seeds) - 1; bo_n[n] += not bocap_
            # moves: the family moves, or the person moves away or leaves home (and it works)
            mvk = (L["MOVES"][s] & live_) | (((mk_ == MIDX["moved away"]) | (mk_ == MIDX["left home"]) | (mk_ == MIDX.get("came home", -2))) & succ & ~idle & live_)
            mv_own_ = (((mk_ == MIDX["moved away"]) | A_MOVE[s, a]) & succ & ~idle & live_)   # their own move
            if P["far_share"] < 1 and mv_own_.any():   # E6: only some of one's own moves are to a new town (newcomer .93 vs .60)
                mv_own_ &= far_rng.random(N) < P["far_share"]
            mv_fam_ = L["MOVES"][s] & live_
            if P["move_near"] and mv_fam_.any():   # K2: the family's move is to a new town fam_far of the time
                mv_fam_ &= fam_rng.random(N) < MVF_[s]
            mv_far = mv_fam_ | mv_own_   # a new town (newcomer); without move_near the family's move always is one
            mvk = mvk | (A_MOVE[s, a] & succ & ~idle & live_)
            if mvk.any():
                ii_ = np.nonzero(mvk)[0]
                if P["move_near"]:   # K2: a move within the town keeps half the circle (new neighbours, the same friends)
                    kp_ = np.where(mv_far[ii_], 0.0, 0.5)[:, None]
                    circle[ii_] = kp_ * circle[ii_] + (1 - kp_) * random_messages(rng, len(ii_))
                    nic[ii_] = (0.5 + 0.5 * kp_) * nic[ii_] + (0.5 - 0.5 * kp_) * circle[ii_]
                    res[ii_, TIE] = np.maximum(0, res[ii_, TIE] - np.where(mv_far[ii_], 0.2, 0.1))
                else:
                    circle[ii_] = random_messages(rng, len(ii_)); nic[ii_] = 0.5 * nic[ii_] + 0.5 * circle[ii_]
                    res[ii_, TIE] = np.maximum(0, res[ii_, TIE] - 0.2)
                ago["move"][ii_] = t; n_moves[ii_] += 1
                if WON:   # the world: a new place (a far move: another locality; leaving or coming home: nearby)
                    for n in ii_:
                        why_ = "came home" if mk_[n] == MIDX.get("came home", -2) else "left home" if mk_[n] == MIDX.get("left home", -2) else None
                        WL.move(int(n), local=not bool(mv_far[n]), why=why_)
            if WON:   # the world: the close circle judges the act, rank in settings moves, a lever pushes (world-fields.md);
                # a want the moment answered is met or refused; what happened in each logged life's world goes in its events
                for r_ in WL.on_act(~idle & live_ & ~dead, s, a, ma, succ, L, closed_s[ar, a] >= 0 if closed_s is not None else np.zeros(N, bool)):
                    if isinstance(r_, dict) and r_.get("n") in events:
                        events[r_["n"]].append(dict(sphere_lever=r_) if r_.get("kind") == "sphere lever" else dict(world_push=r_))
                    if (DB_ON and isinstance(r_, dict) and r_.get("kind") == "sphere lever" and r_.get("lever") == "found"
                            and r_.get("sphere") in ("prod", "comm") and float(r_.get("went", 0)) >= 0.5):
                        n_ = int(r_["n"])   # a found act that went well founds a workshop or shop, worth a year's income
                        if res[n_, MON] >= DP_["found_lv"] and (hk[n_] < 0).any() and not (hk[n_] == 2).any():
                            hk[n_, int(np.argmax(hk[n_] < 0))] = 2
                            db_log(n_, kind="holding gained", holding=H_KIND[2], why="founded")
                for n in list(WL.pending):
                    ev_ = WL.resolve(n, s[n], a[n], succ[n], idle[n])
                    if SAC_ON_ and isinstance(ev_, dict) and ev_.get("kind") == "sacred":
                        sac_fx(n, ev_)
                        if n in events:
                            events[n].append(dict(sacred=ev_))
                        continue
                    if ev_ is not None and n in events:
                        events[n].append(dict(cast_want=ev_))
                if SAC_ON_:   # S5: offers decided off-screen this week (no moment for them)
                    for ev_ in WL.PP.sac_take():
                        n_ = int(ev_["n"])
                        if not dead[n_]:
                            sac_fx(n_, ev_)
                        if n_ in events:
                            events[n_].append(dict(sacred=ev_))
                world_cast(WL.drain())   # the act's own cast events (the world's events came at the week's start)
            # tags: habit pulls harder, a door opens the niche, identity teaches more, binds holds and costs autonomy
            tg_ = L["TAG"][s, a] & (~idle & live_)[:, None]
            habit += P["tag_habit"] * tg_[:, :1] * ma
            hedon_n = hedon_n * (1 - 1 / 52) + (tg_[:, 0] & L["HEDON"][s, a])
            bodyhab_n = bodyhab_n * 0.75 + (tg_[:, 0] & (L["BODY"][s, a] > 0))
            dr_ = tg_[:, 1] & succ
            nic[dr_] += P["tag_door"] * (ma[dr_] - nic[dr_])
            dI = dI * (1 + P["tag_identity"] * tg_[:, 2:3])
            bd_ = tg_[:, 3] & succ
            bind_m = bind_m * np.exp(-1 / 520) + bd_
            bind_c = np.where(bd_[:, None], 0.8 * bind_c + 0.2 * ma, bind_c)
            need[:, NIDX["autonomy"]] -= P["bind_aut"] * np.minimum(bind_m, 3)
            # v7 discipline: an act the Library flags self_control "+" builds it (half when it does not work out), "-" wears it
            sc_ = L["SC"][s, a] * (~idle & live_); stf_ = TST[stage] / TST[2]
            up_ = sc_ > 0; dn_ = sc_ < 0
            dsc[up_] += P["disc_tag"] * stf_[up_] * np.where(succ[up_], 1.0, 0.5) * (P["disc_range"][1] - dsc[up_])
            dsc[dn_] -= P["disc_tag"] * stf_[dn_] * (dsc[dn_] - P["disc_range"][0])
            # closed options that fail backfire by kind: law (freedom, ties, money), approval (belonging, ties), means (money)
            clk_ = closed_s[ar, a]; bf_ = (clk_ >= 0) & ~succ & ~idle & live_
            if bf_.any():
                law_, app_, mea_ = bf_ & (clk_ == 0), bf_ & (clk_ == 1), bf_ & (clk_ == 2)
                res[law_, FRE] -= 0.15; res[law_, TIE] -= 0.1; res[law_, MON] -= 0.05; stress[law_] += 0.3
                bk_ = np.minimum(clu_[ar, a], 1.0)[app_] if CLU_ON else 1.0   # N1b: a light frown backfires lightly
                need[app_, NIDX["belonging"]] -= 0.1 * bk_; res[app_, TIE] -= 0.08 * bk_; stress[app_] += 0.15 * bk_
                res[mea_, MON] -= 0.1; stress[mea_] += 0.15
            res[:, HEA] -= P["body_hurt"] * L["BODY"][s, a] * (~succ & ~idle & live_)
            if SAC_ON_:   # S5: the acts that cost something real (money, ties or stress from the act itself, over
                # sacred_par's thresholds) count toward a line in their colour's ways, and heal a wound in it (People.sac_act)
                sp_ = WL.PP.sac_par
                rd_ = L["PAY"][s, a] + np.where(succ[:, None], L["WIN"][s, a], L["LOSE"][s, a])
                dm_, dt_, ds_ = rd_[:, MON].copy(), rd_[:, TIE].copy(), np.zeros(N)
                if closed_s is not None:   # a closed option's backfire, as above
                    ck2_ = closed_s[ar, a]; b2_ = (ck2_ >= 0) & ~succ
                    bk2_ = np.minimum(clu_[ar, a], 1.0) if CLU_ON else 1.0
                    dm_ -= 0.05 * (b2_ & (ck2_ == 0)) + 0.1 * (b2_ & (ck2_ == 2))
                    dt_ -= 0.1 * (b2_ & (ck2_ == 0)) + 0.08 * bk2_ * (b2_ & (ck2_ == 1))
                    ds_ += 0.3 * (b2_ & (ck2_ == 0)) + 0.15 * bk2_ * (b2_ & (ck2_ == 1)) + 0.15 * (b2_ & (ck2_ == 2))
                cost_ = (dm_ <= -sp_["cost_money"]) | (dt_ <= -sp_["cost_ties"]) | (ds_ >= sp_["cost_stress"])
                lv2_ = ~idle & live_ & ~dead
                if sp_["cost_closed"] and closed_s is not None:   # any closed option's backfire counts (sacred_par)
                    cost_ = cost_ | b2_
                    WL.PP._sac_count("cost closed", b2_ & lv2_)
                for nm_, m_ in (("money", dm_ <= -sp_["cost_money"]), ("ties", dt_ <= -sp_["cost_ties"]),
                                ("stress", ds_ >= sp_["cost_stress"])):
                    WL.PP._sac_count(f"cost {nm_}", m_ & lv2_)   # (for the checks)
                for ev_ in WL.sacred_act(lv2_, ma, cost_):
                    sac_fx(int(ev_["n"]), ev_)
                    if int(ev_["n"]) in events:
                        events[int(ev_["n"])].append(dict(sacred=ev_))
            res = _uclip(res, 0, 1)
            # after a lost job, most people find work again within a year or two (quietly, when the batch has no event for it)
            rj_ = np.nonzero(REJOB_ON & ~held[:, CAR] & ~retired & (end_t[:, CAR] > NEVER // 2) & (age < P["retire_age"] - 1)
                             & (rng.random(N) < P["rejob"] / 52))[0]
            for n in rj_:
                held[n, CAR] = True; I[n, CAR] = 0.2; sat[n, CAR] = 0.6; since[n, CAR] = t
                prof[n, CAR] = P["commit_mix"][0] * nic[n] + P["commit_mix"][1] * w[n] + P["commit_mix"][2] * nic[n]
                commit_log.append((int(n), t, CAR, "start", prof[n, CAR].round(2).tolist(), 0.2))
                if n in events:
                    events[n].append(dict(commitment=dict(age=round(age, 2), kind="career", what="start", through="found new work",
                                                          profile=prof[n, CAR].round(2).tolist())))
            newk_[rj_, CAR] = True
            if JM_ON:   # F9.19: a change of employer; the career and its strength go on, the workplace is new
                jm_ = np.nonzero(held[:, CAR] & ~retired & ~dead & (t - since[:, CAR] >= 52) & (t - ago["job"] >= 52) & (age < P["retire_age"])
                                 & (jm_rng.random(N) < float(np.interp(age, JM_A, JM_F)) / 52))[0]
                for n in jm_:
                    commit_log.append((int(n), t, CAR, "moved", prof[n, CAR].round(2).tolist(), round(float(I[n, CAR]), 2)))
                    if n in events:
                        events[n].append(dict(commitment=dict(age=round(age, 2), kind="career", what="moved",
                                                              through="changed employer")))
                    if WON:
                        WL.PP.leave(int(n), "work", t, "changed employer")   # a new work setting is joined next
                ago["job"][jm_] = t
            # what happened lately, and how long things have been as they are
            if P["base_rates"]:
                ago["le"][had_ev] = t
            ago["commit"][newk_.any(1)] = t; ago["child"][newk_[:, KID]] = t; ago["job"][newk_[:, CAR]] = t
            ago["win"][succ & ~idle & (stakes >= 0.9)] = t
            ago["hard_win"][succ & ~idle & (p_true < 0.5)] = t
            ago["fail_big"][~succ & ~idle & (stakes >= 0.9)] = t
            ago["fail_body"][~succ & ~idle & ((L["BODY"][s, a] > 0) | ((A_DEATH[s, a] > 0) if BAT else False))] = t
            ago["fail_long"][long_miss] = t
            ago["hard"][stress > 1.5] = t
            fails13 = fails13 * (1 - 1 / 13) + (~succ & ~idle & (delta < -0.3))
            stress_slow = 0.9 * stress_slow + 0.1 * stress
            for nm_, c_ in (("quiet", ~((had_ev if P["base_rates"] else False) | newk_.any(1) | mvk)),
                            ("lo_meaning", need[:, NIDX["meaning"]] < 0.45), ("vlo_meaning", need[:, NIDX["meaning"]] < 0.3),
                            ("lo_belong", need[:, NIDX["belonging"]] < 0.35), ("lo_peace", peace < 0.45), ("hi_stress", stress > 1.5),
                            ("lo_time", res[:, TIM] < 0.15), ("lo_auto", need[:, NIDX["autonomy"]] < 0.35),
                            ("ok_needs", (need[:, [0, 1, 3]] >= 0.55).all(1)), ("ok_body", (res[:, HEA] > 0.75) & (stress < 0.6)),
                            ("easing", stress < stress_slow - 0.01),
                            ("flat_comp", np.abs(need[:, NIDX["competence"]] - comp_ref) < 0.03)):
                streak[nm_] = np.where(c_, streak[nm_] + 1, 0)
            comp_ref = np.where(streak["flat_comp"] > 0, comp_ref, need[:, NIDX["competence"]])
            hist_m = np.where(idle[:, None], hist_m, hist_m + (ma - hist_m) / 520)
            ep_ = np.maximum(ea, 0); ep_ = ep_ / np.maximum(ep_.sum(1, keepdims=True), 1e-9)
            hist_e = np.where(idle[:, None], hist_e, hist_e + (ep_ - hist_e) / 520)
        imp = rng.random(N) < P["impose_p"]
        if imp.any():
            which = rng.choice(nI, size=imp.sum(), p=pb)
            need[imp] += 0.5 * L["IMP"][which]
            stress[imp] += 0.15
            res[imp, FRE] = _uclip(res[imp, FRE] + 0.5 * IMP_FREE[which], 0, 1)
            ii = np.nonzero(imp)[0]
            lost = ii[(which == 1) & held[ii, CAR] & JOBLOSS_ON & (rng.random(len(ii)) < 0.25)]    # an institution betrays its promise
            end(lost, [CAR] * len(lost), "lost job", t)
