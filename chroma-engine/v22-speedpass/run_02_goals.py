# run_02_goals.py: part 2 of 18 of engine._run, the life loop.
# Goal slots, dreams, the goal helpers (glog, new_goal, plans, end_goal, end).
# Lines here are _run's own, unchanged and at their own indent: engine.py joins the parts in order (engine.RUN_PARTS)
# and compiles them as one, so a name used here may be set in an earlier part. Never import or run it alone.
    # ---- v7 goals: one row of slots per person; kind -1 = empty, 0 dream, 1 passion, 2 plan
    GON = bool(P["goals"])
    NGS = P["max_dreams"] + P["max_passions"] + P["max_plans"]; GMAX = (P["max_dreams"], P["max_passions"], P["max_plans"])
    gk = np.full((N, NGS), -1); gm = np.full((N, NGS, C), 0.2); gd = np.full((N, NGS), -1)   # kind, the ways it calls for, domain
    gs = np.zeros((N, NGS)); gp = np.zeros((N, NGS)); gv = np.zeros((N, NGS)); ga = np.full((N, NGS), 0.5)   # strength, progress,
    # meaningful success gathered (valuation), and how freely it was taken in (1 harmonious, 0 obsessive; Vallerand 2003)
    gi = np.zeros((N, NGS)); gpk = np.zeros((N, NGS))                          # investment (sunk), peak strength
    gb = np.zeros((N, NGS), int); gh = np.zeros((N, NGS), int); ghz = np.zeros((N, NGS), int); gx = np.zeros((N, NGS), int)  # born, due, horizon, extensions
    gsrc = np.zeros((N, NGS), int); gtrig = np.full((N, NGS), -1); gpar = np.full((N, NGS), -1); gby = np.zeros((N, NGS), int)
    # the Library's dreams (chroma-library/dreams.py, Emren 10-06 22:19, via batch): the setting's sparks, and the concrete
    # dreams a new one is named by (gname: its index in DRM_, carried into its passion and plans; -1 = plain naming)
    DTR_ = L.get("DREAM_TRIGGERS") or DREAM_TRIGGERS
    TRIG_SRC = np.array([GSRC[tr[1]] for tr in DTR_])
    TRIG_W = np.array([tr[2] for tr in DTR_], float)                   # triggers x stages
    TRIG_TILT = np.array([parse(tr[3]) if tr[3] else np.zeros(C) for tr in DTR_])
    DRM_ = L.get("DREAMS") or []
    DG_ON = bool(P.get("dream_grow")) and bool(DRM_)   # v22.5, F6: dreams that grow up
    if DG_ON:   # the Library's added dreams join, so every age has dreams of every colour (dreams.py DREAMS_MORE)
        DRM_ = list(DRM_) + list(L.get("DREAMS_MORE") or [])
    if DRM_:
        DRM_X = np.array([parse(d_["means"]) for d_ in DRM_]); DRM_X = DRM_X / DRM_X.sum(1, keepdims=True)   # its ways, as shares
        DRM_M = DRM_X - 1 / C
        DRM_M = DRM_M / np.linalg.norm(DRM_M, axis=1, keepdims=True)    # each dream's lean among the colors
        DRM_D = np.array([KIDX.get(d_["domain"], -1) for d_ in DRM_])
        DRM_S = np.array([[nm_ in d_["stages"].split() for nm_ in STAGE_NAMES] for d_ in DRM_])
    if DG_ON:   # F6: the youngest age each dream can start at (by its kind), the play dreams, each spark's subjects and ages
        DK_ = L.get("DREAM_KIND") or {}; KF_ = L.get("KIND_FROM") or {}
        DRM_FROM = np.array([float(KF_.get(DK_.get(d_["name"], ""), 0.0)) for d_ in DRM_])
        DRM_PLAY = np.array([DK_.get(d_["name"]) == "play" for d_ in DRM_])
        PLAY_UNTIL_ = float(L.get("PLAY_UNTIL") or 0.0)
        ix_ = {d_["name"]: i_ for i_, d_ in enumerate(DRM_)}; TD_ = L.get("TRIGGER_DREAMS") or {}
        TRIG_SUBJ = [[ix_[x_] for x_ in TD_.get(tr_[0], ()) if x_ in ix_] for tr_ in DTR_]
        TRIG_AGE = np.array([(L.get("TRIGGER_AGES") or {}).get(tr_[0], (0.0, 1e9)) for tr_ in DTR_], float)
    gname = np.full((N, NGS), -1)
    gplay = np.zeros((N, NGS), bool)   # F6: a play dream started before PLAY_UNTIL (short-lived)
    def dream_name(mix, dom, st):
        """The nearest concrete dream: of this setting, able to start at this stage, of this domain; nearest in colors, by
        the way it leans (a dream's mix is broad, so plain distance would favour the broadest dreams). F6 (dream_grow):
        and of a kind they are old enough for."""
        if not DRM_:
            return -1
        ok_ = (DRM_D == dom) & DRM_S[:, st]
        if DG_ON:
            ok_ = ok_ & (DRM_FROM <= age)
        if not ok_.any():
            return -1
        return int(np.argmax(np.where(ok_, DRM_M @ (mix / mix.sum() - 1 / C), -np.inf)))
    def dream_phrase(n, j):
        """What the goal in slot j is called: the dream's name, its passion phrase once sealed, its plan phrase as a
        five-year plan, its life phrase as a life goal."""
        d_ = DRM_[gname[n, j]]
        return d_["name"] if gk[n, j] == 0 else d_["passion"] if gk[n, j] == 1 else d_["life"] if ghz[n, j] == 3 else d_["plan"]
    gid = np.zeros((N, NGS), int); glast = np.zeros((N, NGS), int)
    gtt = np.full((N, NGS), -1)                                              # a plan aimed at a title (pathways): its id
    gch = np.zeros((N, NGS)); gph = np.zeros((N, NGS)); gfelt = np.zeros((N, NGS)); gfelt0 = np.zeros((N, NGS))   # felt chances, step odds, odds
    gsr = np.zeros((N, NGS, L["S"]))                                         # how much each situation offers a step toward it
    lost_m = np.full((N, 3, C), 0.2); lost_d = np.full((N, 3), -1); lost_s = np.zeros((N, 3)); lost_t = np.zeros((N, 3))
    lost_on = np.zeros((N, 3), bool); lost_id = np.zeros((N, 3), int)    # dreams, passions and plans let go of (regret, revival)
    lost_nm = np.full((N, 3), -1)                                         # and the concrete dream each was (gname)
    pres_c = np.zeros((N, C)); pres_d = np.zeros((N, NK)); pres_n = np.zeros(N)   # how often chances in each color and domain come
    regret = np.zeros(N); goal_log = []; gid_next = [1]
    HAS_STEP = np.stack([(L["COMMIT"] == d_).any(1) for d_ in range(NK)], 1).astype(float)   # S x NK: a situation can start it
    SH_REFL = np.array([SH_STATES.index(str((L["src"][i_] if i_ < len(L["src"]) else {}).get("holds") or "").strip())
                        if L["TIER"][i_] == TIERS.index("inner") and str((L["src"][i_] if i_ < len(L["src"]) else {}).get("holds") or "").strip()
                        in SH_STATES else -1 for i_ in range(L["S"])], int)   # the shadow a reflection moment sees, else -1
    SH_NEW = HAS_STEP.max(1)                                                                  # shadows: a moment that opens something new
    SPRIOR = step_prior(L, P)
    MS_ = L["M"] * L["MASK"][..., None]
    def goal_rel_S(mix, dom):
        """For seeking: how much each situation offers a step toward a goal."""
        if dom >= 0:
            return HAS_STEP[:, dom].copy()
        return _uclip((5 * np.einsum("skc,c->sk", MS_, mix) - 1) / 2, 0, 1).max(1)
    def glog(n, j, what, **extra):
        rec = dict(life=int(n), id=int(gid[n, j]), age=round(t / 52, 2), what=what, kind=G_KINDS[gk[n, j]],
                   domain=KNAMES[gd[n, j]] if gd[n, j] >= 0 else "a pursuit", mix=gm[n, j].round(2).tolist(),
                   source=G_SOURCES[gsrc[n, j]], strength=round(float(gs[n, j]), 2), **extra)
        if gtrig[n, j] >= 0:
            rec["trigger"] = DTR_[gtrig[n, j]][0]
            if what == "begins" and gk[n, j] == 0 and len(DTR_[gtrig[n, j]]) > 4:
                rec["say"] = DTR_[gtrig[n, j]][4]                 # the spark, told: one line with {N} for the character
        if gname[n, j] >= 0:
            d_ = DRM_[gname[n, j]]
            rec.update(name=dream_phrase(n, j), dream=d_["name"], passion=d_["passion"], plan=d_["plan"], life_goal=d_["life"])   # (life = the person)
        if gk[n, j] == 2:
            rec.update(horizon=HORIZONS[ghz[n, j]], progress=round(float(gp[n, j]), 2), felt=round(float(gfelt[n, j]), 2))
            if what == "begins":   # what the felt odds leave out (for the foreseen outcome's hint of reality: foresee.py)
                og_ = 0.5 * (w[n] + softmax(y[n]))
                rec.update(by_player=bool(gby[n, j]), self_control=round(float(ctrl[n]), 3), free_time=round(float(res[n, TIM]), 3),
                           stress=round(float(stress[n]), 3), fit=round(float(_uclip(2 * (gm[n, j] * og_).sum() / og_.max() - 1, -0.5, 1)), 3))
        if gk[n, j] == 1:
            rec["harmonious"] = round(float(ga[n, j]), 2)
        goal_log.append(rec)
        if n in events:
            events[n].append(dict(goal=rec))
    def new_goal(n, kind, mix, dom, src, hz=1, trig=-1, par=-1, by=0, s0=0.4, inherit=-1, target=-1, name=-1):
        """Open a slot for a new goal; when the kind is full, the new one replaces the weakest if it is stronger."""
        mine = np.nonzero(gk[n] == kind)[0]
        if len(mine) >= GMAX[kind]:
            j = mine[np.argmin(gs[n, mine])]
            if gs[n, j] >= s0 or gby[n, j]:
                return -1
            end_goal(n, j, "pushed aside")
        free = np.nonzero(gk[n] < 0)[0]
        if not len(free):
            return -1
        j = free[0]
        gk[n, j] = kind; gm[n, j] = mix / mix.sum(); gd[n, j] = dom; gs[n, j] = s0; gpk[n, j] = s0
        gsrc[n, j] = src; gtrig[n, j] = trig; gpar[n, j] = par; gby[n, j] = by; gb[n, j] = t; glast[n, j] = t
        gname[n, j] = name if name >= 0 else gname[n, par] if par >= 0 else dream_name(mix, dom, stage[n]) if kind == 0 else -1
        gplay[n, j] = DG_ON and kind == 0 and gname[n, j] >= 0 and DRM_PLAY[gname[n, j]] and age < PLAY_UNTIL_
        gp[n, j] = 0.0; gi[n, j] = 0.0; gx[n, j] = 0
        gv[n, j] = gv[n, inherit] if inherit >= 0 else 0.0; ga[n, j] = ga[n, inherit] if inherit >= 0 else 0.5
        gid[n, j] = gid_next[0]; gid_next[0] += 1
        gsr[n, j] = goal_rel_S(gm[n, j], dom); gtt[n, j] = target
        if target >= 0:   # a plan aimed at a title seeks the moments that open a way into it, and its kind's beginnings
            gsr[n, j] = np.maximum(GR["DOORS"][target].astype(float), 0.3 * (HAS_STEP[:, TK_[target]] if TK_[target] < NK else 0.0))
        if kind == 2:
            init_plan(n, j, hz)
        glog(n, j, "begins", **({"aims": GR["names"][target]} if target >= 0 else {}))
        if AIM_ON:   # aims v1: the aim it reads as, from below
            aim_from_goal(n, j)
        return j
    def plan_odds(n, mix, dom, hz, s):
        """A person's first sense of a plan's chances (changes nothing; the game previews a plan with it): how often their
        weeks have offered such steps, how a step in its ways looks to them (skill, past feedback, outlook), the weeks to
        the deadline and the felt odds of reaching it in time. mix sums to 1."""
        hw = HORIZON_W[hz]
        weeks = hw if hw is not None else max(52, int((P["life_end"] - t / 52) * 52))
        pn = max(pres_n[n], 1e-9)
        ch = (pres_d[n, dom] if dom >= 0 else (mix * pres_c[n]).sum()) / pn
        mis1 = (P["mis_focus"] * (0.5 - thr[n]) + mix @ (P["mis_mem"] * mem_rel()[n] - P["mis_scar"] * scar[n])) if MIS_ON else 0.0
        ph = 1 / (1 + np.exp(-P["gain"] * ((mix * (sig[n] + fb[n])).sum() - 0.5) - TON * P["o_bias"] * (outlook[n] - P["o_ref"]) - mis1))
        if dom >= 0:   # what they know of such chances, from their own weeks or from people around them; and they imagine
            ch = max(ch, SPRIOR[min(stage[n] + 1, NS - 1), dom], SPRIOR[stage[n], dom])   # looking harder than before
            ch *= 1 + P["g_seek_ev"] * s
        felt = float(felt_odds(ch, ph, weeks, int(np.ceil(P["g_size"][hz] / STEP_INC)), dom, outlook[n], P))
        return ch, ph, weeks, felt
    def init_plan(n, j, hz):
        """A plan's deadline, and the person's first sense of their chances (plan_odds)."""
        ghz[n, j] = hz
        gch[n, j], gph[n, j], wk_, gfelt[n, j] = plan_odds(n, gm[n, j], gd[n, j], hz, gs[n, j])
        gfelt0[n, j] = gfelt[n, j]; gh[n, j] = t + wk_
        gp[n, j] = 0.0; gi[n, j] = 0.0; gx[n, j] = 0
    def seal(n, how, only=None):
        """2A: tries that worked and felt like one's own, sealed by a rite (or a turning point), make a dream a passion."""
        # a second passion takes far more than the first (most people have one, few have two or more; Vallerand 2003)
        cand = [j for j in np.nonzero(gk[n] == 0)[0] if gv[n, j] >= P["seal_v"] and gs[n, j] >= P["seal_s"] and (only is None or j in only)]
        for j in sorted(cand, key=lambda j_: -gv[n, j_]):
            held_p = gk[n] == 1   # one at a time: each passion held raises the bar, and a new love must rival the old
            if gv[n, j] < max(P["seal_v"] * (1 + P["seal_more"] * held_p.sum()), P["seal_rival"] * gv[n, held_p].max(initial=0.0)):
                continue
            mine = np.nonzero(gk[n] == 1)[0]
            if len(mine) >= GMAX[1]:
                jw = mine[np.argmin(gs[n, mine])]
                if gs[n, jw] >= gs[n, j]:
                    continue
                end_goal(n, jw, "pushed aside")
            gk[n, j] = 1; gs[n, j] = max(gs[n, j], 0.6); gpk[n, j] = max(gpk[n, j], gs[n, j]); glast[n, j] = t
            glog(n, j, "became a passion", sealed_by=how)
            if AIM_ON:
                aim_from_goal(n, j)
        if AIM_ON:   # aims v1: a rite makes an aim set by the player theirs, once a try at it worked
            aim_rite(n, how)
    def to_plan(n, j):
        """Coming of age: a dream still strong becomes a five-year plan (a plan is not yet a commitment)."""
        glog(n, j, "became a plan")
        if gd[n, j] >= 0 and held[n, gd[n, j]]:
            gd[n, j] = -1
        gk[n, j] = 2; gsrc[n, j] = GSRC["dream"]; gpar[n, j] = -1
        gsr[n, j] = goal_rel_S(gm[n, j], gd[n, j]); init_plan(n, j, 2)
        glog(n, j, "begins")
        if AIM_ON:
            aim_from_goal(n, j)
    def quit_(n, j, what, letgo):
        """Giving up costs what was put in, less for those who have learned to let go (Wrosch et al. 2003)."""
        stress[n] += P["g_quit"] * gi[n, j] * (1 - letgo)
        need[n, NIDX["meaning"]] -= 0.05 * min(gi[n, j], 1.0)
        if NW_ON: nw_mark(NW_GOAL)
        outlook[n] += 0.05 * gs[n, j] * (0 - outlook[n]) * TON
        end_goal(n, j, what)
    def end_goal(n, j, what, keep=None):
        """Close a goal. A dream, passion or plan that mattered is kept among the things let go of (regret, revival)."""
        glog(n, j, what)
        if gk[n, j] == 2 and P["disc_rate"]:   # discipline is learned: a plan kept strengthens it, one given up weakens it
            if what == "achieved":
                dsc[n] += P["disc_rate"] * (P["disc_range"][1] - dsc[n])
            elif what in ("let go", "not reached in time"):
                dsc[n] -= P["disc_rate"] * (dsc[n] - P["disc_range"][0])
        if keep is None:
            keep = (gk[n, j] == 1) or (gk[n, j] == 0 and gpk[n, j] >= 0.45) or (gk[n, j] == 2 and (gi[n, j] > 0.5 or gsrc[n, j] in (GSRC["dream"], GSRC["passion"], GSRC["old dream"])))
        if keep and what not in ("achieved", "became a passion", "became a plan"):
            q_ = np.argmin(np.where(lost_on[n], lost_s[n], -1.0))
            lost_m[n, q_] = gm[n, j]; lost_d[n, q_] = gd[n, j]; lost_s[n, q_] = gpk[n, j]; lost_t[n, q_] = t / 52
            lost_on[n, q_] = True; lost_id[n, q_] = gid[n, j]; lost_nm[n, q_] = gname[n, j]
        for j2 in np.nonzero(gpar[n] == j)[0]:
            gpar[n, j2] = -1
        gk[n, j] = -1; gs[n, j] = 0.0; gpar[n, j] = -1; gby[n, j] = 0; gtt[n, j] = -1; gname[n, j] = -1
        if AIM_ON:
            gal[n, j] = -1
        ago["goal_end"][n] = t
    ar = np.arange(N)
    decay_B = 0.5 ** (1 / P["crisis_half"])
    nI = len(L["IMP"])
    pb = np.ones(nI) / nI if P["impose_bias"] is None else softmax(np.asarray(P["impose_bias"], float))
    real = (L["MASK"] & (L["M"].std(-1) > 1e-9)).reshape(-1)          # real options (not padding, not "do nothing")
    REQ_ALL = L["REQ"].reshape(-1, NR)[real]; M_ALL = L["M"].reshape(-1, C)[real]
    REQ_ROWS = np.nonzero((REQ_ALL > 0).any(1))[0]; REQ_SUB = REQ_ALL[REQ_ROWS]   # speed pass: options that need means
    def doors(nic, res):
        """For each color: chance that an option acted in that color's way is open to this person
        (the niche lets it happen, and the person has the means it needs)."""
        accn = _uclip(P["access_base"] + P["access_k"] * (nic - 0.2), 0.05, 1.0)
        rg = np.ones((len(res), len(REQ_ALL)))    # speed pass: an option that needs nothing is open to all (1.0 exactly)
        rg[:, REQ_ROWS] = np.where(REQ_SUB[None] > 0, 1 / (1 + np.exp(-P["req_g"] * (res[:, None, :] - REQ_SUB[None]))), 1.0).prod(-1)
        return accn * (rg @ M_ALL) / M_ALL.sum(0)[None]
    def end(ns, ks, why, t):
        for n, kk in zip(ns, ks):
            end_t[n, kk] = t; end_why[n, kk] = WHY.index(why) if why in WHY else -1
            if why == "retired": ago["retire"][n] = t
            if why in ("lost job", "broke up", "widowed"): ago["loss"][n] = t
            if kk == PAR and why in ("left", "broke up"): ago["breakup"][n] = t
            if why in ("left", "lost job", "broke up"):
                stress[n] += 0.5 * I[n, kk] * (0.5 + 2.5 * (prof[n, kk] * softmax(k[n])).sum())
                if why == "left":
                    B[n] += 0.5 * I[n, kk]                      # leaving opens the person up for a while
                    steady[n] *= 1 - 0.3 * I[n, kk] * TON       # and shakes how firmly they hold who they are
                    if kk in (COM, FAI): need[n, NIDX["meaning"]] -= 0.3 * I[n, kk]
                    if NW_ON: nw_mark(NW_COMMIT)
                if kk in (PAR, COM): res[n, TIE] -= 0.15
                if kk == CAR: res[n, MON] -= 0.15
            if why == "retired":
                pension[n] = I[n, kk] * max(0.5, 1 - P["pension_cut"] * max(0.0, P["retire_age"] - t / 52)); retired[n] = True
            if kk == FAI:
                left_given[n] = why == "left" and faith_given[n]; faith_drifted[n] = bool(drift_now[n])   # how the last one ended
                faith_given[n] = False                          # a faith taken up again is one's own
            commit_log.append((int(n), t, int(kk), why, prof[n, kk].round(2).tolist(), round(float(I[n, kk]), 2)))
            if EYES_ON_ and WL is not None and kk in (CAR, PAR, FAI) and why in ("left", "broke up"):   # S3: their places
                WL.PP.eyes_see([n], prof[n, kk][None], [0.5], {CAR: "left job", PAR: "left partner", FAI: "left faith"}[kk])   # read
            if n in events:                                                  # the leaving by what was walked away from
                events[n].append(dict(commitment=dict(age=round(t / 52, 2), kind=KNAMES[kk], what=why,
                                                      profile=prof[n, kk].round(2).tolist(), strength=round(float(I[n, kk]), 2))))
                if kk == FAI and why == "left" and drift_now[n]:
                    events[n][-1]["commitment"]["drifted"] = True   # it stopped mattering; no decision was made
            held[n, kk] = False; I[n, kk] = 0.0

