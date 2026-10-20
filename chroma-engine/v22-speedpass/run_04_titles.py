# run_04_titles.py: part 4 of 18 of engine._run, the life loop.
# Titles and perks: their rules, r_gain, r_lose, r_act, r_entry.
# Lines here are _run's own, unchanged and at their own indent: engine.py joins the parts in order (engine.RUN_PARTS)
# and compiles them as one, so a name used here may be set in an earlier part. Never import or run it alone.
    # ---- titles and perks (after v7): roles others recognise, and what a person can do or has access to
    RON = BAT and bool(P["roles"]) and "ROLES" in L
    EARN_ON = False; LOG_CAP = np.log(P["earned_cap"] / (1 - P["earned_cap"]))
    def earned(z, er):
        """An act's odds (logit z) with the earned lift er: a lift never carries the odds past earned_cap."""
        if not np.ndim(er) and er == 0.0:
            return z
        return z + np.where(er > 0, np.minimum(er, np.maximum(LOG_CAP - z, 0.0)), er)
    AQ_ON = BAT and bool(P["adjectives"]) and bool(L.get("ADJ_ANY"))   # v7: acts or situations require an adjective
    role_log = []
    RW_ON = bool(P["role_why"]) and RON and bool(events)   # role_why: causes recorded for the played lives (events) only
    rw_why = {}    # role_why: (life, item, "gained" or "lost") -> the cause, set just before the change and taken by r_note
    rw_mk = {}     # role_why: (life, mark) -> (week, moment, way) the mark was last left in
    rw_use = {}    # role_why: life -> week each perk was last in use (its ways in the life's recent acts)
    LONG_ = -1; missed_t = np.full(N, -1)                    # the long-shot perk; the last title each life missed on a long shot
    C5F_ = -1                                                # C5: the title that founds a movement ("founder of a movement")
    tries_ct = None                                          # failed tries per life and title or perk (try_lift)
    if RON:
        GR = L["ROLES"]; NT_, NP_, NI_ = GR["NT"], GR["NP"], GR["NI"]
        if P.get("green_jobs") and GR.get("rule_when"):   # v22.4: the green entry jobs' rules and roads (ROLES_WHEN)
            GR = dict(GR, rule=[GR["rule_when"].get(i_, r_) for i_, r_ in enumerate(GR["rule"])])
        if P.get("cause_fit") and GR.get("rule_fit"):   # E2: the cause audit's tightened conditions (ROLES_FIT)
            GR = dict(GR, rule=[GR["rule_fit"].get(i_, r_) for i_, r_ in enumerate(GR["rule"])])
        if P.get("sph_titles") and GR.get("rule_sph"):   # item 15: the sphere titles follow their own rules
            sr_ = {**GR["rule_sph"], **(GR.get("rule_sph_when") or {})} if P.get("green_jobs") else GR["rule_sph"]
            GR = dict(GR, rule=[sr_.get(i_, r_) for i_, r_ in enumerate(GR["rule"])])   # (earth_rules.SPH_TITLE_ROLES)
        r_has = np.zeros((N, NI_), bool); r_ever = np.zeros((N, NI_), bool)
        r_since = np.full((N, NI_), NEVER); r_end = np.full((N, NI_), NEVER)
        p_acc = np.zeros((N, NP_), bool); p_lev = np.zeros((N, NP_)); p_sus = np.full((N, NP_), NEVER)   # access, skill, suspended until
        tries_ct = np.zeros((N, NI_), np.int8)
        TK_ = GR["tkind"]; KT_ = np.zeros((NT_, NK)); ck_ = TK_ < NK; KT_[np.nonzero(ck_)[0], TK_[ck_]] = 1.0
        ODD4 = 4.0 * GR["odds"]; INDP = GR["ind"][NT_:]; WAYS_ = GR["ways"]
        PKIND_ = np.asarray(GR["pkind"]); CAREER_ = (np.asarray(GR["tkind"]) == 0).astype(float)   # v10: skills (0), standings (2); careers
        PW_, PN_, REF_ = GR["PW"], GR["PN"], GR["refines"]          # title profiles (colors) and facets (refines another title)
        REFM_ = GR["REFM"]                                          # items x titles: the titles a facet can sit on (any of them)
        _hm = GR.get("S_HOLDM"); _ht = GR.get("S_TEN")               # holds: (any of) and tenure: (point 6)
        if _hm is None:   # an older batch.py: the first name of holds: or requires: only
            _hm = np.zeros((L["S"], NI_), bool); _rq = GR["S_REQ"]; _hm[np.nonzero(_rq >= 0)[0], _rq[_rq >= 0]] = True
            _ht = np.full((L["S"], 2), np.nan)
        _tn = ~np.isnan(_ht[:, 0]); _hh = _hm.any(1)
        HOLDS_ = np.nonzero(_hh & ~_tn)[0]; HOLDM_ = _hm[HOLDS_].T.astype(np.float32)
        HOLD_C = np.nonzero(HOLDM_.any(1))[0]; HOLDM_C = HOLDM_[HOLD_C]   # speed pass: the rows that can count (0/1 sums, exact)
        TENS_ = [(int(s_), np.nonzero(_hm[s_])[0], float(_ht[s_, 0]), float(_ht[s_, 1])) for s_ in np.nonzero(_hh & _tn)[0]]
        if TENS_:   # speed pass: the tenure gates in one pass (each moment once; its titles side by side)
            TEN_S = np.array([e_[0] for e_ in TENS_], int); TEN_I = np.concatenate([e_[1] for e_ in TENS_])
            TEN_ST = np.cumsum([0] + [len(e_[1]) for e_ in TENS_[:-1]])
            TEN_LO = np.concatenate([np.full(len(e_[1]), e_[2]) for e_ in TENS_])
            TEN_HI = np.concatenate([np.full(len(e_[1]), e_[3]) for e_ in TENS_])
        f_pend = []                                                  # facets an act gave before their title came (newlywed, wedding week)
        PMASK_ = np.arange(PW_.shape[1])[None, :] < PN_[:, None]
        r_prof = np.zeros((N, NI_), int); r_drift = np.zeros((N, NI_), int)
        def fit_best(v_, i_):   # fit of colors v_ (C, or N x C) with the title's best-fitting profile
            f_ = np.tensordot(np.asarray(v_), PW_[i_].T, axes=1)
            return np.where(PMASK_[i_], f_, -np.inf).max(-1)
        MEM_K = np.isin(GR["pkind"], (0, 1)) & (GR["half"] > 0)      # skills and credentials leave a skill that fades by its half-life
        A_GR1 = np.full((L["S"], L["K"]), -1)                       # the perk an act grants (regaining is easier while the skill lasts)
        for (si_, ki_), fx_ in GR["A_FX"].items():
            gr_ = [j_ for op_, j_, _ in fx_["ok"] if op_ == "grants" and j_ >= NT_]
            if gr_: A_GR1[si_, ki_] = gr_[0]
        RULE_LOSS = np.array([GR["rule"][NT_ + p_]["lose"] is not None for p_ in range(NP_)], bool)   # lost only as the rule says
        ONCE_HOLD_ = [np.nonzero(GR["S_HOLDM"][:, i_] & np.asarray(L["ONCE"], bool))[0] for i_ in range(NI_)]
        KIND_NAMES_ = list(KNAMES) + ["status"]; KINDN_ = np.array(GR["kindname"][:NT_])   # batch.TITLE_KINDS
        EARN_ON = "A_EARN" in GR and bool((GR["HELP_N"] > 0).any() or (L.get("WINDOW_REF", np.zeros(1)) > 0).any())
        RID = GR["ID"]; LONG_ = RID.get("a long shot that missed", -1)
        C5F_ = RID.get("founder of a movement", -1) if P.get("c5_faith") else -1
        LONGF_ = np.zeros((L["S"], L["K"]), bool)            # options whose failure grants the long-shot perk (grants_if_fails:)
        for (si_, ki_), fx_ in GR["A_FX"].items():
            LONGF_[si_, ki_] = LONG_ >= 0 and any(op_ == "grants" and j_ == LONG_ for op_, j_, _ in fx_["fail"])
        LONGT_ = (GR["A_TITLE"] >= 0) | LONGF_
        TIER_ = np.asarray(GR.get("TIER", np.zeros(NI_, np.int8)))   # 1 a pack career, 2 a summit (batch._targets)
        AMS_ = GR.get("A_MISSED", np.zeros((L["S"], L["K"]), bool)); AMS_ON = bool(AMS_.any())
        TZM_ = np.minimum(np.asarray(GR.get("TIER_Z", np.zeros(NI_)), float),   # the budget's move on the odds, for
                          float(GR.get("BUDGET", {}).get("act_cap", 0.0)))         # {missed} (batch._chance)
        def missed_at(base_, ss_, aa_=None):
            """An option's title (A_TITLE or A_EARN rows) with title: {missed} read per person: the title that life last
            missed on a long shot (packs 09:39: the second try earns, counts tries and takes the tier lift)."""
            if not AMS_ON:
                return base_
            if aa_ is None:   # N x K rows for the moments ss_
                return np.where(AMS_[ss_] & (missed_t[:, None] >= 0), missed_t[:, None], base_)
            return np.where(AMS_[ss_, aa_] & (missed_t >= 0), missed_t, base_)
        OW_ = RID.get("out of work", -1); SOLDIER_ = RID.get("soldier", -1); CALL_ = SIDX.get("the call to serve", -1); CAP_K = np.array([P["community_titles"] if kk_ == COM else 1 for kk_ in range(NK)])
        ENGINE_GRANTED = {"widowed", "divorced", "retiree", "out of work", "newcomer", "veteran", "left the faith"}
        LZ_ = [i_ for i_ in range(NI_) if GR["rule"][i_]["lose"] is not None]
        AGES_T = [tuple(r_) for r_ in GR["ages"]]   # speed pass: each title's ages unpacked once (the same numbers)
        BG = [i_ for i_ in range(NI_) if GR["names"][i_] not in ENGINE_GRANTED and
              not (i_ < NT_ and TK_[i_] < NK and GR["rule"][i_]["rate"] is None)]      # items with a background rule
        TI_F = {list(GR["names"]).index(k_): float(f_) for k_, f_ in (P["ti_fit"] or {}).items() if k_ in list(GR["names"])}
        def r_rate(i_):
            r_ = GR["rule"][i_]
            if r_["rate"] is not None:
                return r_["rate"] * TI_F[i_] if i_ in TI_F else r_["rate"]   # F9: ti_fit
            lo_, hi_ = GR["ages"][i_]; span_ = max(1.0, min(hi_, lo_ + 40) - lo_)
            rt_ = -np.log(1 - min(GR["share"][i_], 0.95)) / span_
            return rt_ * TI_F[i_] if i_ in TI_F else rt_
    def r_note(n, i, what, how):
        role_log.append((int(n), t, int(i), what, how))
        if n in events:
            rec_ = dict(age=round(t / 52, 2), name=GR["names"][i], kind=GR["kindname"][i], what=what, how=how)
            if RW_ON:
                why_ = rw_why.pop((int(n), int(i), what), None)
                if why_ is not None:
                    rec_["why"] = why_; rec_["t"] = t
            events[n].append(dict(role=rec_))
    WL = None                                             # the outer world's link (set below when the world is on)
    EYES_LOSE_SKIP = {"replaced", "time passed", "outgrew it", "retired", "slipped away", "found work", "it ended",
                      "gave it up"}   # S3:
    # titles that end as the time or a commitment's end runs, or given up (the leaving itself is read, by end())
    def r_lose(n, i, why, succ=-1):
        if not r_has[n, i] and not (i >= NT_ and p_acc[n, i - NT_]):
            return
        r_has[n, i] = False; r_end[n, i] = t
        if (EYES_ON_ and WL is not None and i < NT_ and why not in EYES_LOSE_SKIP and not why.startswith("the ")
                and not why.startswith("became ") and why not in WHY):   # S3: a title lost in its own way (taken away, given
            WL.PP.eyes_see([n], PW_[i, r_prof[n, i]][None], [0.5], "title lost")   # up, its rule): read as walked away from
        if i < NT_:   # its facets go with it (no longer a newlywed once no longer married), unless they sit on another title
            for f_ in np.nonzero(REFM_[:, i] & r_has[n])[0]:   # held, or on the one that follows it (living together, married)
                if not (REFM_[f_] & r_has[n, :NT_]).any() and not (succ >= 0 and REFM_[f_, succ]):
                    r_lose(n, f_, "the " + GR["names"][i] + " ended")
        if i >= NT_:
            p_acc[n, i - NT_] = False; p_sus[n, i - NT_] = NEVER
            if not MEM_K[i - NT_]:
                p_lev[n, i - NT_] = 0.0                      # nothing left once access is gone (money spent, a bond broken)
        r_note(n, i, "lost", why)
        if i == SOLDIER_ and (t - r_since[n, i] >= 104          # however the service ends, after two years or more,
                              or (CALL_ >= 0 and t - r_since[n, i] >= 26 and sit_last[n, CALL_] >= r_since[n, i] - 8)):
            r_give(n, "veteran", "served")                     # or a conscript's term of half a year or more (W39)
    def r_gain(n, i, how, mix=None):
        if r_has[n, i]:
            return
        if P["title_ages"] and not (GR["ages"][i, 0] <= t / 52 <= GR["ages"][i, 1]):   # never outside the catalogue's ages
            return                                           # (C-X4: Emren's sanity check; the act still works)
        if CRS_ON and i < NT_ and TK_[i] < NK and CRS_J[TK_[i]] >= 0 and not held[n, TK_[i]]:
            j_ = CRS_J[TK_[i]]                               # F16: a title that would start a partnership, children or a faith
            if crs_rng.random() >= np.exp(CRS_MU[j_] + crs_own[n, j_] + (5 * w[n] - 1) @ CRS_T[j_]):   # leans as the acts do
                return
        if i < NT_ and REF_[i] >= 0 and not (REFM_[i] & r_has[n, :NT_]).any():
            f_pend.append((n, i, how, mix, t))               # a facet only on top of the title it refines: it waits a little
            return
        if i < NT_:                                          # the profile that fits: the act's colors, else the person's
            src_ = w[n] if mix is None else mix
            r_prof[n, i] = int(np.argmax(np.where(PMASK_[i], PW_[i] @ src_, -np.inf))); r_drift[n, i] = 0
        if i < NT_ and TK_[i] < NK:                          # a title of a commitment kind refines (or starts) that commitment
            kk = TK_[i]
            same = np.nonzero(r_has[n, :NT_] & (TK_ == kk) & (REF_[:NT_] < 0))[0]
            if REF_[i] < 0 and len(same) >= CAP_K[kk]:
                r_lose(n, same[np.argmin(r_since[n, same])], "replaced", succ=i)
            if not held[n, kk]:
                held[n, kk] = True; I[n, kk] = 0.2; sat[n, kk] = 0.6; since[n, kk] = t
                if RE_ON and kk == CAR:   # F8: an act that takes a job ends the retirement (one work status)
                    retired[n] = False
                pm_ = P["commit_mix"]
                prof[n, kk] = w[n].copy() if mix is None else pm_[0] * mix + pm_[1] * w[n] + pm_[2] * nic[n]
                commit_log.append((int(n), t, int(kk), "start", prof[n, kk].round(2).tolist(), 0.2))
                if n in events:
                    events[n].append(dict(commitment=dict(age=round(t / 52, 2), kind=KNAMES[kk], what="start", through=GR["names"][i],
                                                          profile=prof[n, kk].round(2).tolist())))
            if WAYS_[i].sum() > 0:                           # the role's expected ways become part of the commitment's profile
                held_k = np.nonzero(r_has[n, :NT_] & (TK_ == kk))[0]
                tw_ = (PW_[held_k, r_prof[n, held_k]].sum(0) + PW_[i, r_prof[n, i]]) / (len(held_k) + 1)
                prof[n, kk] = 0.5 * prof[n, kk] + 0.5 * tw_
        elif i >= NT_:
            p_ = i - NT_
            how = "regained" if p_lev[n, p_] > 0.05 and r_ever[n, i] else how
            p_acc[n, p_] = True; p_lev[n, p_] = 1.0; p_sus[n, p_] = NEVER
        first_ = not r_ever[n, i]
        r_has[n, i] = True; r_ever[n, i] = True; r_since[n, i] = t
        if len(ONCE_HOLD_[i]) and first_:                    # once: on a moment held by a title means once per title in a
            once_done[n, ROOT[ONCE_HOLD_[i]]] = False         # life (a second kind of career meets its new-stage moments
                                                              # again; the same title regained does not: Library 23:20)
        if i in TH_TITLE and first_:                         # a rung of a pathway: its threshold season opens (once:
            sea_open(n, NS + i)                              # back to the same line of work is no new crossing)
        r_note(n, i, "gained", how)
        if WL is not None:   # the world: a migrant's, refugee's or citizen's title moves the life between societies
            WL.on_title(int(n), GR["names"][i])
            if EYES_ON_ and (i < NT_ or GR["names"][i] == "someone with a record") and how != "arrested":
                # S3: their places see a title won (its profile's colours, else the act's), or a record (a crime found out:
                # the act's colours where an act gave it, else their own; a killing found out is read where it is caught)
                rec_ = GR["names"][i] == "someone with a record"
                src_ = mix if mix is not None else (PW_[i, r_prof[n, i]] if i < NT_ and not rec_ else w[n])
                src_ = src_ if np.sum(src_) > 0 else w[n]
                WL.PP.eyes_see([n], np.asarray(src_, float)[None], [0.0 if rec_ else 1.0], "crime" if rec_ else "title")
        if i < NT_ and f_pend:                               # facets an act gave while waiting for this title come with it
            for e_ in [e_ for e_ in f_pend if e_[0] == n and REFM_[e_[1], i]]:
                f_pend.remove(e_); r_gain(n, e_[1], e_[2], e_[3])
        for j_ in (GR["rule"][i]["grants"] if i < NI_ else []):
            r_gain(n, j_, "came with " + GR["names"][i])
    def r_close(n, i, why):
        """The last title of a commitment is gone: so is the commitment."""
        kk = TK_[i] if i < NT_ else NK
        if kk < NK and held[n, kk] and not (r_has[n, :NT_] & (TK_ == kk) & (REF_[:NT_] < 0)).any():
            end([n], [kk], why, t)
            if why == "retired":
                r_give(n, "retiree", "retired")
    def r_give(n, nm, how):
        if nm in RID:
            r_gain(n, RID[nm], how)
    def fx_targets(n, s_, j_):
        """What an act field acts on: the item named, the title held that brought the person here ({title}, -2), or every
        title of a kind held (kind:<kind>, -10 - the kind's index; the title itself, its facets go with it)."""
        if j_ >= 0:
            return [j_]
        if j_ == -2:
            h_ = held_title(n, s_)
            return [h_] if h_ >= 0 else []
        if j_ == -3:                                   # {missed}: the title of the last failed long shot
            return [int(missed_t[n])] if missed_t[n] >= 0 else []
        kn_ = KIND_NAMES_[-10 - j_]
        return [int(i_) for i_ in np.nonzero(r_has[n, :NT_] & (KINDN_ == kn_) & (REF_[:NT_] < 0))[0]]
    def held_title(n, s_):
        """The title (or perk) that brings person n to moment s_ (its holds:, with tenure: one held that long); the title
        itself before a facet on it, then the one held longest (explain.title_held tells the same one)."""
        ii_ = np.nonzero(GR["S_HOLDM"][s_] & r_has[n])[0]
        lo_, hi_ = GR["S_TEN"][s_]
        if not np.isnan(lo_):
            y_ = (t - r_since[n, ii_]) / 52; ii_ = ii_[(y_ >= lo_) & (y_ <= hi_)]
        if len(ii_) > 1:
            ii_ = sorted(ii_, key=lambda i_: (GR["refines"][i_] >= 0, r_since[n, i_]))
        return int(ii_[0]) if len(ii_) else -1
    def black_k():
        """black_edge: 1 + black_edge x how Black-led each person is now (Black share .2 -> 0, .5 or more -> 1)."""
        return 1.0 + P["black_edge"] * _uclip((w[:, 2] - 0.2) / 0.3, 0.0, 1.0)
    def r_weight(i_):
        """Who is likelier to gain it: practice in its ways (skills), colors that fit its ways, money, or ties."""
        wk_ = GR["rule"][i_]["weight"]
        if wk_ is None and i_ >= NT_ and GR["pkind"][i_ - NT_] == 0:
            wk_ = "practice"
        ind_ = GR["ind"][i_]
        if wk_ == "practice" and ind_.sum() > 0:
            return np.exp(_uclip(1.5 * (5 * (hist_m @ ind_) / ind_.sum() - 1), -2, 2))
        if wk_ == "colors" and WAYS_[i_].sum() > 0:
            return np.exp(_uclip(1.5 * (5 * fit_best(w, i_) - 1), -2, 2))
        if wk_ == "money":
            return np.exp(3 * (res[:, MON] - 0.5))
        if wk_ == "ties":
            return np.exp(3 * (res[:, TIE] - 0.5))
        return 1.0
    def r_act(n, op, j, yrs, how, mix=None):
        if op in ("title", "grants"):
            r_gain(n, j, how, mix)
        elif op == "drops":
            if r_has[n, j]:
                r_lose(n, j, "gave it up"); r_close(n, j, "left")
        elif op == "takes" and j >= NT_:
            r_lose(n, j, "taken away")
        elif op == "suspends" and j >= NT_ and p_acc[n, j - NT_]:
            p_sus[n, j - NT_] = t + int(yrs * 52); r_has[n, j] = False; r_note(n, j, "suspended", how)
        elif op in ("takes", "suspends"):
            r_lose(n, j, "taken away")
    def r_entry(n, kk, mix, ns_, move=False):
        """The first title of a commitment that has just started: one its rules allow, likelier the better its ways fit.
        move=True: a change inside a commitment already held (a new job), only to titles whose rules now hold."""
        cand = [i_ for i_ in range(NT_) if TK_[i_] == kk and GR["rule"][i_]["entry"] and REF_[i_] < 0 and GR["ages"][i_, 0] <= age <= GR["ages"][i_, 1]
                and not r_has[n, i_] and not (move and not GR["rule"][i_]["has_req"])]
        if not move and kk == CAR and P["occ_keep"] > 0:   # a new job is mostly in the same line of work as the last one
            prev_ = [i_ for i_ in range(NT_) if TK_[i_] == kk and REF_[i_] < 0 and not r_has[n, i_] and r_ever[n, i_]
                     and t - r_end[n, i_] <= 52 * P["occ_back"] and GR["ages"][i_, 0] <= age <= GR["ages"][i_, 1]
                     and TIER_[i_] != 2 and not GR["rule"][i_]["starts"]]   # never a summit or a seat won (packs 11:02)
            prev_ = [i_ for i_ in prev_ if ev_cond(GR["rule"][i_]["req"], ns_)[n]]   # and only while its rules still hold
            if prev_ and rng.random() < P["occ_keep"]:
                r_gain(n, max(prev_, key=lambda i_: r_end[n, i_]), "back to the same line of work")
                return
        ok_ = [i_ for i_ in cand if ev_cond(GR["rule"][i_]["req"], ns_)[n]]
        if not ok_ and not move:   # nobody's rules hold: a title with no rules of its own, else any but a pack career or
            ok_ = [i_ for i_ in cand if not GR["rule"][i_]["has_req"] and TIER_[i_] == 0] or \
                  [i_ for i_ in cand if TIER_[i_] == 0]   # summit (packs 11:02: no career from nothing)
        if not ok_:
            return
        wt_ = np.array([GR["share"][i_] * GR["rule"][i_]["norm"] * (np.exp(min(3.0, 2 * (5 * float(fit_best(mix, i_)) - 1))) if WAYS_[i_].sum() > 0 else 1.0)
                        for i_ in ok_])
        pick_ = ok_[int(rng.choice(len(ok_), p=wt_ / wt_.sum()))]
        if ID2 and TROLE_ON and TROLE_[pick_] >= 0:   # N1b: a job the world reserves for the other sex, as they are expected,
            # is closed by approval: taken only with closed_acc ^ units, else the person goes for another job (by weight)
            rs_n = min(1.0, float(np.broadcast_to(RS0, (N,))[n]) + (0.0 if WON else 0.5) * faith_given[n] * I[n, FAI])
            a_n = float(np.broadcast_to(AT0, (N,))[n]) if named_g[n] else 0.0
            ex_n = np.zeros(2); ex_n[int(not female[n])] += 1 - a_n; ex_n[int(female[n])] += a_n if gender_self[n] == 1 else 0.0
            tr_n = TROLE_[ok_]
            f_ = P["closed_acc"] ** (P["role_k"] * rs_n * np.where(tr_n >= 0, ex_n[1 - _uclip(tr_n, 0, 1)], 0.0))
            if ent_rng.random() >= f_[ok_.index(pick_)]:
                rest_ = [j_ for j_, i_ in enumerate(ok_) if i_ != pick_ and f_[j_] >= 1.0]
                if not rest_:
                    return
                w2_ = wt_[rest_]
                pick_ = ok_[rest_[int(rng.choice(len(rest_), p=w2_ / w2_.sum()))]]
        else:
            f_ = None
        acc_k_ = "acc_move" if move else "acc_first"
        ac_ = GR["rule"][pick_].get(acc_k_, 1.0)   # a route that overfills a title (Library next3
        if ac_ < 1 and ent_rng.random() >= ac_:    # §3): the job comes without that title
            if not P["acc_redraw"]:
                return
            out_ = {pick_}   # acc_redraw (v22.4): the next-best fit among the rest, each with its own acceptance
            while True:
                rest_ = [j_ for j_, i_ in enumerate(ok_) if i_ not in out_ and (f_ is None or f_[j_] >= 1.0)]
                if not rest_:
                    return
                w2_ = wt_[rest_]
                pick_ = ok_[rest_[int(ent_rng.choice(len(rest_), p=w2_ / w2_.sum()))]]
                ac_ = GR["rule"][pick_].get(acc_k_, 1.0)
                if not (ac_ < 1 and ent_rng.random() >= ac_):
                    break
                out_.add(pick_)
        r_gain(n, pick_, "changed jobs" if move else "came with the " + KNAMES[kk])

    # ---- aims v1 (aims; chroma-ideas/next-table-2026-10-19/plan.md section 5): up to aims_par slots a life, each an aim
    # of the batch's catalogue (L["AIMS"]: the Library's and the packs' ladders) with its strength, the steps reached, and
    # whether it is the character's own (grown from below, or sparked) or still set by the player; a calling. The heights
    # (Known, Notable, Historic) are read with it, or alone (heights, read-only)
    AIM_ON = bool(P["aims"]) and GON and RON and bool(L.get("AIMS"))
    HT_ON = (bool(P["heights"]) or AIM_ON or (P.get("world_answers") and P.get("wa_phase2") and P.get("world"))) and RON   # read-only
    # (the world answers' second phase reads Known from it)
    AP_ = P["aims_par"]
    AIM = ak = astr = astep = aown = aby = atest = acall = abirth = aim_best = gal = ht_t = None; aim_log = []
    if AIM_ON:
        AIM = L["AIMS"]; NAIM_ = AIM["A"]; AQ_ = int(AP_["slots"])
        ak = np.full((N, AQ_), -1); astr = np.zeros((N, AQ_)); astep = np.zeros((N, AQ_), int)   # aim, strength, steps
        aown = np.zeros((N, AQ_), bool); aby = np.zeros((N, AQ_), bool)   # the character's own; set by the player
        atest = np.zeros((N, AQ_), bool); acall = np.zeros((N, AQ_), bool); abirth = np.zeros((N, AQ_), int)   # a spark's
        # try worked (the next rite makes it their own); a calling; the week it was taken
        aim_best = np.zeros((N, NAIM_), int)   # the most steps each aim reached in this life
        gal = np.full((N, NGS), -1)            # the aim each goal slot reads as (-1 none)
        AIM_LEAN = AIM["face"] - 1 / C; AIM_LEAN = AIM_LEAN / np.linalg.norm(AIM_LEAN, axis=1, keepdims=True)
        DRM_AIM = [[] for _ in DRM_]           # the aims each concrete dream can grow into (the aims' dreams)
        ix_ = {d_["name"]: i_ for i_, d_ in enumerate(DRM_)}
        for a_, x_ in enumerate(AIM["aims"]):
            for d_ in x_["dreams"]:
                if d_ in ix_:
                    DRM_AIM[ix_[d_]].append(a_)
        SPK_A = np.full(L["S"], -1); SPK_ROLE = {}   # a spark moment's aim; each of its options' dream: test, seal or drop
        for a_, s_ in enumerate(AIM["spark"]):
            if s_ >= 0:
                SPK_A[s_] = a_
                for k_, nt_ in enumerate(L["notes"][s_]):
                    if (nt_ or {}).get("dream") in ("test", "seal", "drop"):
                        SPK_ROLE[(int(s_), k_)] = nt_["dream"]
    if HT_ON:   # the names of each height (realm_earth.HEIGHT_NAMES) in this catalogue; Notable also every summit title
        HT_I = [np.array([RID[x_] for x_ in HEIGHT_NAMES[h_] if x_ in RID], int) for h_ in ("Known", "Notable", "Historic")]
        HT_I[1] = np.union1d(HT_I[1], np.nonzero(TIER_ == 2)[0]).astype(int)
        ht_t = np.full((N, 3), -1)             # the week each height was first reached, -1 never
    def aim_fit(mix):
        """How each aim's face fits a mix of colours: the cosine of their leans (1 the same lean)."""
        lm_ = mix / mix.sum() - 1 / C; nr_ = float(np.linalg.norm(lm_))
        return AIM_LEAN @ (lm_ / nr_) if nr_ > 1e-9 else np.zeros(NAIM_)
    def aim_of_goal(n, j):
        """The aim goal slot j reads as: one its concrete dream can grow into (the best fit among them), else the best fit
        of its domain if it fits at least aims_par fit; -1 none."""
        f_ = aim_fit(gm[n, j])
        c_ = DRM_AIM[gname[n, j]] if gname[n, j] >= 0 else []
        if c_:
            return max(c_, key=lambda a_: f_[a_])
        ok_ = (AIM["dom"] == gd[n, j]) & (f_ >= AP_["fit"])
        return int(np.argmax(np.where(ok_, f_, -np.inf))) if ok_.any() else -1
    def alog(n, q_, what, **extra):
        x_ = AIM["aims"][ak[n, q_]]
        rec = dict(life=int(n), age=round(t / 52, 2), what=what, aim=x_["name"], slot=int(q_), own=bool(aown[n, q_]),
                   by_player=bool(aby[n, q_]), steps=int(astep[n, q_]), of=len(x_["steps"]),
                   strength=round(float(astr[n, q_]), 2), **extra)
        aim_log.append(rec)
        if n in events:
            events[n].append(dict(aim=rec))
    def aim_take(n, a_, s0, own, by=False, src="dream"):
        """Life n takes aim a_ (one already held is strengthened to s0). When the slots are full the weakest gives way if
        it is weaker, has no step reached, is no calling and is not the player's (the player's own choice gives way to
        nothing but the player). Returns the slot, -1 for no room. Its steps already reached are read at the next month,
        without meaning."""
        q_ = np.nonzero(ak[n] == a_)[0]
        if len(q_):
            q_ = int(q_[0]); astr[n, q_] = max(astr[n, q_], s0)
            aby[n, q_] |= by
            return q_
        fr_ = np.nonzero(ak[n] < 0)[0]
        if len(fr_):
            q_ = int(fr_[0])
        else:
            cd_ = np.arange(AQ_) if by else np.nonzero(~aby[n] & (astep[n] == 0) & ~acall[n])[0]
            if not len(cd_):
                return -1
            q_ = int(cd_[np.argmin(astr[n, cd_])])
            if astr[n, q_] >= s0 and not by:
                return -1
            aim_end(n, q_, "pushed aside")
        ak[n, q_] = a_; astr[n, q_] = s0; astep[n, q_] = 0; aown[n, q_] = own; aby[n, q_] = by
        atest[n, q_] = acall[n, q_] = False; abirth[n, q_] = t
        alog(n, q_, "begins", source=src)
        return q_
    def aim_end(n, q_, what):
        alog(n, q_, what)
        gal[n, gal[n] == ak[n, q_]] = -1
        ak[n, q_] = -1; astr[n, q_] = 0.0; astep[n, q_] = 0
        aown[n, q_] = aby[n, q_] = atest[n, q_] = acall[n, q_] = False
    def aim_from_goal(n, j):
        """From below: the aim a dream, passion or plan of the character's reads as is taken (a player's plan: set by the
        player, not yet their own), at half the goal's strength."""
        a_ = aim_of_goal(n, j)
        gal[n, j] = a_
        if a_ >= 0:
            aim_take(n, a_, 0.5 * gs[n, j], own=not gby[n, j], by=bool(gby[n, j]), src=G_KINDS[gk[n, j]])
    def aim_pull():
        """Each moment's pull from the aims held: a way into an aim's next step (ROLES DOORS), by its strength (a player's
        aim not yet their own at reluctant), and the spark moment of an aim not yet their own (spark_seek)."""
        pu_ = np.zeros((N, L["S"]), np.float32)
        for q_ in range(AQ_):
            on_ = np.nonzero(ak[:, q_] >= 0)[0]
            if not len(on_):
                continue
            a_ = ak[on_, q_]
            wq_ = astr[on_, q_] * np.where(aown[on_, q_], 1.0, AP_["reluctant"])
            pu_[on_] += (wq_[:, None] * AIM["door"][a_, np.minimum(astep[on_, q_], AIM["K"])]).astype(np.float32)
            sp_ = ~aown[on_, q_] & (AIM["spark"][a_] >= 0)
            if sp_.any():
                pu_[on_[sp_], AIM["spark"][a_[sp_]]] += AP_["spark_seek"] * astr[on_[sp_], q_]
        return pu_
    def aim_spark():
        """A spark moment's pick (its options' dream: test, seal or drop). A try that works opens the aim (their own) or
        brings it on, and readies one set by the player to become theirs at the next rite; a seal that works makes it
        theirs; a try that fails weakens it; a drop lets a player's aim go and weakens their own."""
        for n in np.nonzero(~idle & (SPK_A[s] >= 0))[0]:
            a_ = int(SPK_A[s[n]]); ro_ = SPK_ROLE.get((int(s[n]), int(a[n])))
            if ro_ is None:
                continue
            q_ = np.nonzero(ak[n] == a_)[0]; q_ = int(q_[0]) if len(q_) else -1
            if ro_ in ("test", "seal") and succ[n]:
                if q_ < 0:
                    q_ = aim_take(n, a_, 0.3, own=True, src="spark")
                    if q_ < 0:
                        continue
                else:
                    astr[n, q_] = min(1.0, astr[n, q_] + AP_["spark_up"])
                if not aown[n, q_]:
                    if ro_ == "seal":
                        aown[n, q_] = True; alog(n, q_, "became their own", how="a try that worked, sealed")
                    else:
                        atest[n, q_] = True
            elif ro_ in ("test", "seal") and q_ >= 0:
                astr[n, q_] *= 0.9
            elif ro_ == "drop" and q_ >= 0:
                if aown[n, q_]:
                    astr[n, q_] *= 0.7
                else:
                    aim_end(n, q_, "let go")
    def aim_rite(n, how):
        """A rite of passage or a turning point makes an aim set by the player theirs, once a try at it has worked."""
        for q_ in np.nonzero((ak[n] >= 0) & atest[n] & ~aown[n])[0]:
            aown[n, q_] = True; alog(n, q_, "became their own", how=how)
    def aim_month(ns_):
        """Each month: an aim's strength follows the goals that read as it, else fades by its half-life; the steps reached
        (held or once held, the step's req then, or for the Known step leading in the aim's sphere: rung 4),
        each new one meeting meaning by its height; a calling (an aim of their own toward a height, held as a passion for
        call_yrs)."""
        for q_ in range(AQ_):
            on_ = ak[:, q_] >= 0
            if not on_.any():
                continue
            lk_ = on_[:, None] & (gal == ak[:, q_][:, None]) & (gk >= 0)
            fd_ = astr[:, q_] * 0.5 ** (4 / 52 / np.where(aown[:, q_], AP_["half"], AP_["half_set"]))
            astr[:, q_] = np.where(on_, np.where(lk_.any(1), np.maximum(np.where(lk_, gs, 0.0).max(1), fd_), fd_), 0.0)
            for n in np.nonzero(on_ & (astr[:, q_] < AP_["drop"]))[0]:
                aim_end(n, q_, "faded")
        met_ = False
        for a_ in np.unique(ak[ak >= 0]):
            rows_, qs_ = np.nonzero(ak == a_)
            x_ = AIM["aims"][a_]; best_ = np.zeros(len(rows_), int)
            for k_, st_ in enumerate(x_["steps"]):
                ok_ = r_ever[rows_][:, st_["any"]].any(1) if len(st_["any"]) else np.zeros(len(rows_), bool)
                if st_["req"] is not None and ok_.any():
                    ok_ &= ev_cond(st_["req"], ns_)[rows_]
                if st_["h"] == 1 and AIM["sph"][a_] >= 0 and WON and hasattr(WL.PP, "rung"):   # rungs: the spheres' hours
                    ok_ |= np.floor(np.asarray(WL.PP.rung)[rows_, AIM["sph"][a_]]) >= 4
                best_ = np.where(ok_, k_ + 1, best_)
            for n, q_, b_ in zip(rows_, qs_, best_):
                o_ = int(astep[n, q_])
                if b_ <= o_:
                    continue
                astep[n, q_] = b_; aim_best[n, a_] = max(aim_best[n, a_], b_)
                if abirth[n, q_] > t - 4:   # taken since the last month: what was already reached, without meaning
                    alog(n, q_, "stands at", say=x_["steps"][b_ - 1]["say"])
                    continue
                h_ = max(st_["h"] for st_ in x_["steps"][o_:b_])
                need[n, NIDX["meaning"]] += AP_["meet"][h_] * (1 - need[n, NIDX["meaning"]]); met_ = True
                astr[n, q_] = min(1.0, astr[n, q_] + 0.1)
                alog(n, q_, "step", say=x_["steps"][b_ - 1]["say"], height=AIM_HEIGHTS[h_ - 1] if h_ else None)
        if met_ and NW_ON:
            nw_mark(NW_GOAL)
        cl_ = (ak >= 0) & aown & ~acall & AIM["calling"][np.maximum(ak, 0)]
        for n, q_ in zip(*np.nonzero(cl_)):
            ps_ = (gk[n] == 1) & (gal[n] == ak[n, q_])
            if ps_.any() and (t - gb[n, ps_]).max() >= 52 * AP_["call_yrs"]:
                acall[n, q_] = True; alog(n, q_, "became a calling")
    def ht_month():
        """The heights reached (read-only): Known, leading a sphere (rung 4) or a Known name (Emren 10-19); Notable, a Notable
        name or a summit title; Historic, a Historic name or leading a movement; each height counts the ones above it."""
        hs_ = [r_ever[:, HT_I[h_]].any(1) if len(HT_I[h_]) else np.zeros(N, bool) for h_ in range(3)]
        if WON:
            if hasattr(WL.PP, "rung"):   # the spheres' rungs (a world without them reads the titles alone)
                hs_[0] = hs_[0] | (np.floor(np.asarray(WL.PP.rung)) >= 4).any(1)
            from world_people_base import G as WG_   # the kinds of the world's settings (a movement's)
            if "movement" in WG_ and hasattr(WL.PP, "slead"):
                hs_[2] = hs_[2] | ((np.asarray(WL.PP.slead) == -2) & (np.asarray(WL.PP.skind) == WG_["movement"])).any(1)
        hs_[1] = hs_[1] | hs_[2]; hs_[0] = hs_[0] | hs_[1]   # at least: a Historic life is Notable, a Notable one Known
        for h_ in range(3):
            nw_ = hs_[h_] & (ht_t[:, h_] < 0)
            ht_t[nw_, h_] = t
            for n in np.nonzero(nw_)[0]:
                if n in events:
                    events[n].append(dict(height=dict(age=round(t / 52, 2), height=AIM_HEIGHTS[h_])))

    HAD_IDX = {}
    NO_FOUND = np.zeros(N, bool)   # C5 founding (earth_rules INNER "a following of your own"): open only with c5_faith
