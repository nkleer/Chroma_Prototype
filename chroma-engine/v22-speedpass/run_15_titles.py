# run_15_titles.py: part 15 of 18 of engine._run, the life loop.
# Titles follow commitments; titles and perks gained and lost in time (role_why records why).
# Lines here are _run's own, unchanged and at their own indent: engine.py joins the parts in order (engine.RUN_PARTS)
# and compiles them as one, so a name used here may be set in an earlier part. Never import or run it alone.
        if RON:   # titles follow commitments: a new one takes its first title; an ended one loses its titles, maybe leaving a status
            tk_ = (r_has[:, :NT_] @ KT_) > 0
            ent_ = held & ~tk_ & ((since == t) | (t % 4 == 0))
            ns_ = cond_ns(t, age, w) if (ent_.any() or t % 4 == 0) else None
            if ent_.any():
                for n, kk in zip(*np.nonzero(ent_)):
                    r_entry(n, kk, ma[n] if since[n, kk] == t and not idle[n] else w[n], ns_)
            for n, kk in zip(*np.nonzero(tk_ & ~held)):
                tl_ = np.nonzero(r_has[n, :NT_] & (TK_ == kk))[0]
                why_ = WHY[end_why[n, kk]] if end_why[n, kk] >= 0 else "it ended"
                nm_ = {GR["names"][i_] for i_ in tl_}
                for i_ in tl_:
                    r_lose(n, i_, why_)
                wed_ = nm_ & {"wife or husband", "married again", "partner of many years", "living together"}
                if why_ == "widowed" and wed_:
                    r_give(n, "widowed", "the partner died")
                elif kk == PAR and why_ in ("broke up", "left") and nm_ & {"wife or husband", "married again", "partner of many years"}:
                    r_give(n, "divorced", "the marriage ended")
                elif why_ == "retired":
                    r_give(n, "retiree", "retired")
                if kk == FAI and why_ == "left" and (left_given[n] or P["faith_drift"] is None):   # the faith they grew up in
                    r_give(n, "left the faith", "drifted away" if faith_drifted[n] else "walked away")
            if "out of work" in RID:
                for n in np.nonzero(r_has[:, RID["out of work"]] & held[:, CAR])[0]:
                    r_lose(n, RID["out of work"], "found work")
            for n in np.nonzero(mv_far)[0]:
                r_give(n, "newcomer", "moved")
            if t % 4 == 0:   # ---- each month: suspensions end, statuses run out, the engine's rules give and take
                # a title's profile follows the person: after about a year in which another of its profiles fits clearly
                # better, they hold it that way (a lab technician who came for the routine stays for the living material)
                for n, i_ in zip(*np.nonzero(r_has[:, :NT_] & (PN_[:NT_] > 1)[None])):
                    f_ = np.where(PMASK_[i_], PW_[i_] @ w[n], -np.inf); b_ = int(np.argmax(f_))
                    r_drift[n, i_] = r_drift[n, i_] + 1 if (b_ != r_prof[n, i_] and f_[b_] - f_[r_prof[n, i_]] > P["profile_margin"]) else 0
                    if r_drift[n, i_] >= 12:
                        if TK_[i_] < NK and held[n, TK_[i_]]:   # the commitment leans the new way (and stays a mix of colors)
                            kk_ = TK_[i_]
                            pr_ = np.maximum(prof[n, kk_] + 0.25 * (PW_[i_, b_] - PW_[i_, r_prof[n, i_]]), 0.0)
                            prof[n, kk_] = pr_ / pr_.sum() if pr_.sum() > 1e-9 else PW_[i_, b_]
                        r_prof[n, i_] = b_; r_drift[n, i_] = 0
                        r_note(n, i_, "reshaped", GR["pwords"][i_][b_] or "in other ways")
                for n, p_ in zip(*np.nonzero((p_sus > NEVER // 2) & (p_sus <= t))):
                    p_sus[n, p_] = NEVER; r_has[n, NT_ + p_] = True; r_note(n, NT_ + p_, "restored", "the suspension ended")
                for n, i_ in zip(*np.nonzero(r_has[:, :NT_] & ((t - r_since[:, :NT_]) / 52 >= GR["lasts"]))):
                    if i_ == OW_ and not held[n, CAR]:
                        continue                                   # out of work lasts while there is no work
                    if RW_ON and n in events:   # role_why: how long it was held, against how long it lasts
                        rw_why[(int(n), int(i_), "lost")] = [dict(k="held", years=round((t - r_since[n, i_]) / 52, 2),
                                                                 lasts=float(GR["lasts"][i_]))]
                    r_lose(n, i_, "time passed")
                for n, i_ in zip(*np.nonzero(r_has[:, :NT_] & (age > GR["ages"][:NT_, 1]))):   # outgrown: a scout at nineteen
                    r_lose(n, i_, "outgrew it")
                    if not (TK_[i_] == CAR and age < P["retire_age"]):   # an apprentice at thirty, a soldier at fifty-five:
                        r_close(n, i_, "retired" if TK_[i_] == CAR else "outgrew it")   # the work goes on under another title
                    if i_ == OW_:
                        r_give(n, "retiree", "reached pension age")
                for n, p_ in zip(*np.nonzero(p_acc & ((age >= GR["retires"]) | (age > GR["ages"][NT_:, 1]))[None])):
                    r_lose(n, NT_ + p_, "retired")                 # the skill stays as memory
                # what slips away on its own: an unused skill, standing, a bond (more when alone), an asset (more when poor);
                # what a rule says how it is lost (good credit, a car, a dog) goes only that way
                pk_ = GR["pkind"]
                use_ = 5 * (hist_m @ INDP.T) / np.maximum(INDP.sum(1), 1)[None]
                if P["skill_room"]:   # skill_room: the skills held in the same ways share the acts that keep them up
                    ip_ = INDP / np.maximum(INDP.sum(1, keepdims=True), 1)
                    crowd_ = ((r_has[:, NT_:] & (pk_ == 0)[None]).astype(float) @ ip_) @ ip_.T   # held skills in each one's ways
                    use_ = use_ * np.minimum(1.0, P["skill_room"] / np.maximum(crowd_, 1e-9))
                mult_ = np.where(pk_[None] == 0, 2 * _uclip(1.5 - use_, 0, 1.5), 1.0)
                mult_ = np.where(pk_[None] == 3, 1 + 2 * (res[:, TIE] < 0.3)[:, None], mult_)
                mult_ = np.where(pk_[None] == 4, 1 + 4 * (res[:, MON] < 0.15)[:, None], mult_)
                base_ = np.select([pk_ == 0, pk_ == 2, pk_ == 3, pk_ == 4], list(P["perk_loss"]), 0.0)
                if RW_ON:   # role_why: the week each skill was last kept up (its ways used enough that it does not slip)
                    for n in events:
                        lu_ = rw_use.setdefault(n, np.full(NP_, NEVER))
                        lu_[use_[n] >= 1.5] = t
                for n, p_ in zip(*np.nonzero(r_has[:, NT_:] & ~RULE_LOSS[None] & (rng.random((N, NP_)) < 1 - np.exp(-base_[None] * mult_ / 13)))):
                    if RW_ON and n in events:   # role_why: held how long, unused how long; a bond alone, an asset short of money
                        lu_ = max(int(rw_use[n][p_]), int(r_since[n, NT_ + p_])) if pk_[p_] == 0 else int(r_since[n, NT_ + p_])
                        rw_why[(int(n), int(NT_ + p_), "lost")] = [dict(   # years: unused (a skill), else held
                            k="unused", years=round((t - lu_) / 52, 2), held=round(float(t - r_since[n, NT_ + p_]) / 52, 2),
                            # as: why it went (a skill unused; a bond while alone; an asset while short of money; else time)
                            **{"as": ("unused" if pk_[p_] == 0 else "alone" if pk_[p_] == 3 and res[n, TIE] < 0.3
                                      else "short of money" if pk_[p_] == 4 and res[n, MON] < 0.15 else "time")})]
                    r_lose(n, NT_ + p_, "slipped away")
                fade_ = MEM_K[None] & ~p_acc & (p_lev > 0)        # a skill without access fades by its half-life
                p_lev *= np.where(fade_, 0.5 ** (1 / (13 * np.maximum(GR["half"], 1e-9)))[None], 1.0)
                if "out of work" in RID:   # still without work half a year after losing a job
                    ow_ = (~held[:, CAR] & ~retired & (end_why[:, CAR] == WHY.index("lost job")) & (t - end_t[:, CAR] >= P["ow_weeks"])
                           & (t - end_t[:, CAR] < P["ow_weeks"] + 4) & (age < P["retire_age"]))
                    for n in np.nonzero(ow_)[0]:
                        r_give(n, "out of work", "no work for half a year" if P["ow_weeks"] < 52 else "no work for a year")
                # a new job inside the career: now and then, to one the person now qualifies for (a graduate becomes a teacher)
                mv_ = held[:, CAR] & (rng.random(N) < P["title_move"] / 13)
                for n in np.nonzero(mv_)[0]:
                    r_entry(n, CAR, w[n], ns_, move=True)
                for i_ in LZ_:   # every item with a rule for losing it, whether or not a background rule gives it
                    ru_ = GR["rule"][i_]
                    hold_ = r_has[:, i_] | (p_acc[:, i_ - NT_] if i_ >= NT_ else False)
                    if np.count_nonzero(hold_):
                        pz_ = hold_ & (rng.random(N) < 1 - (1 - min(ru_["lrate"], 1.0)) ** (1 / 13))
                        for code_, why_ in ru_["lose"]:                  # each way of losing it, in its own words
                            lz_ = pz_ & ev_cond(code_, ns_); pz_ = pz_ & ~lz_
                            for n in np.nonzero(lz_)[0]:
                                r_lose(n, i_, why_)
                                if not (i_ < NT_ and TK_[i_] == CAR and age < P["retire_age"]):   # a physician whose
                                    r_close(n, i_, ru_["lend"])  # registration lapses works on under another title;
                                    # lend: how the commitment ends with it (an engagement broken off: "broke up")
                for i_ in BG:
                    ru_ = GR["rule"][i_]
                    lo_, hi_ = AGES_T[i_]
                    if not (lo_ <= age <= hi_) or (i_ >= NT_ and age >= GR["retires"][i_ - NT_]):
                        continue
                    cand_ = ~r_has[:, i_]
                    if i_ >= NT_:
                        cand_ = cand_ & ~p_acc[:, i_ - NT_]
                    kk_ = TK_[i_] if i_ < NT_ else NK
                    if ru_["after"]:                          # grows from another title (a cook becomes head chef), held
                        cand_ = cand_ & (r_has[:, ru_["after"]] & (t - r_since[:, ru_["after"]] >= 52 * P["rung_min"])).any(1)
                    elif kk_ < NK and not ru_["starts"]:      # a role inside a commitment already held
                        cand_ = cand_ & held[:, kk_]
                    elif kk_ < NK:                            # a role that starts its commitment: not for those whose kind is full
                        cand_ = cand_ & (~held[:, kk_] | ((r_has[:, :NT_] & (TK_ == kk_)).sum(1) < CAP_K[kk_]))
                        if RE_ON and kk_ == CAR:              # F8: no job comes to the retired on its own (only by their act)
                            cand_ = cand_ & ~(retired & ~held[:, CAR])
                    if not np.count_nonzero(cand_):
                        continue
                    base_ = cand_
                    cand_ = cand_ & ev_cond(ru_["req"], ns_)
                    if ru_["more"]:   # a pack's own way into this rule (EXTEND_<PACK>), at its own yearly rate
                        rt_ = r_rate(i_)
                        pr_ = (np.ones(N) if rt_ >= 1 else 1 - np.exp(-rt_ * ru_.get("hz", ru_["norm"]) * r_weight(i_) / 13)) * cand_
                        for code_, rx_ in ru_["more"]:
                            px_ = (base_ & ev_cond(code_, ns_)) * (1 - np.exp(-rx_ / 13))
                            pr_ = 1 - (1 - pr_) * (1 - px_); cand_ = cand_ | (px_ > 0)
                    if not np.count_nonzero(cand_):
                        continue
                    if not ru_["more"]:
                        rt_ = r_rate(i_)
                        pr_ = np.ones(N) if rt_ >= 1 else 1 - np.exp(-rt_ * ru_.get("hz", ru_["norm"]) * r_weight(i_) / 13)
                    for n in np.nonzero(cand_ & (rng.random(N) < pr_))[0]:
                        fr_ = [j_ for j_ in ru_["after"] if r_has[n, j_] and t - r_since[n, j_] >= 52 * P["rung_min"]]
                        for j_ in fr_:
                            r_lose(n, j_, "became " + GR["names"][i_], succ=i_)
                        if RW_ON and n in events and not fr_:   # role_why: the parts of its rule that held, read-only
                            it_ = rw_clause(ru_.get("req_s"), ns_, n, ru_.get("ext_s", ()))
                            if it_ is None:                  # not the rule itself: a pack's own way in (at its own rate)
                                for pk_, src_ in ru_.get("more_s", ()):
                                    it_ = rw_clause(src_, ns_, n)
                                    if it_ is not None:
                                        it_ = [dict(k="pack", pack=pk_, clause=src_)] + it_
                                        break
                            if ru_.get("pack") and not (it_ and it_[0]["k"] == "pack"):   # a rule a pack owns
                                it_ = [dict(k="pack", pack=ru_["pack"], clause=ru_.get("req_s") or "")] + (it_ or [])
                            it_ = it_ or [dict(k="none")]
                            if ru_.get("say"):
                                for x_ in it_:
                                    x_["say"] = ru_["say"]
                            rw_why[(int(n), int(i_), "gained")] = it_
                        r_gain(n, i_, ("grew from " + GR["names"][fr_[0]]) if fr_ else "in time")
                        if RW_ON and not r_has[n, i_] and not any(e_[0] == n and e_[1] == i_ for e_ in f_pend):
                            rw_why.pop((int(n), int(i_), "gained"), None)   # not given after all (ages, a held kind)
                if f_pend:   # a facet an act gave in the week before its title came (newlywed at the wedding): now, or never
                    keep_ = []
                    for (n, i_, how_, mix_, t0_) in f_pend:
                        if (REFM_[i_] & r_has[n, :NT_]).any():
                            r_gain(n, i_, how_, mix_)
                        elif t - t0_ < 8:
                            keep_.append((n, i_, how_, mix_, t0_))
                        elif RW_ON:
                            rw_why.pop((int(n), int(i_), "gained"), None)
                    f_pend[:] = keep_
                if AIM_ON:   # aims v1: strength, steps reached, callings
                    aim_month(ns_)
                if HT_ON:    # the heights reached (read-only)
                    ht_month()
