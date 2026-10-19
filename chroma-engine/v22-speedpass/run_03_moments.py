# run_03_moments.py: part 3 of 18 of engine._run, the life loop.
# The Library's batch: marks, echoes, inner moments, gaps, the moments only a line brings, identity, birth order.
# Lines here are _run's own, unchanged and at their own indent: engine.py joins the parts in order (engine.RUN_PARTS)
# and compiles them as one, so a name used here may be set in an earlier part. Never import or run it alone.
    # ---- the Library's batch format: marks (what an act leaves in a history), echoes, inner moments, who is alive,
    # what ends, tags, closed options, outside events read through the colors. All conditions are the engine's reading
    # (<world>_rules.py) of the Library's plain words
    BAT = "COND" in L
    NEVER = -10 ** 7
    MIDX = {m_: i_ for i_, m_ in enumerate(L["MARKS"])}; NM = len(L["MARKS"]); SIDX = {n_: i_ for i_, n_ in enumerate(L["names"])}
    mark_last = np.full((N, NM), NEVER); mark_first = np.full((N, NM), NEVER); mark_ok = np.zeros((N, NM), bool)
    mark_n = np.zeros((N, NM), np.int32)
    sit_last = np.full((N, L["S"]), NEVER); sit_first = np.full((N, L["S"]), NEVER); once_done = np.zeros((N, L["S"]), bool)
    ROOT = np.asarray(L.get("ROOT", np.arange(L["S"])))                  # each situation's original (itself, or variant_of)
    HASFAM_ = np.bincount(ROOT, minlength=L["S"])[ROOT] > 1               # situations that share their original with another
    def _gap(g_):   # the Library's gap: "2-5", (2, 5) or 3 (years)
        if g_ is None or g_ == "": return (np.nan, np.nan)
        if isinstance(g_, str):
            p_ = [float(x) for x in g_.replace(" ", "").split("-") if x]
            return (p_[0], p_[-1])
        if isinstance(g_, (int, float)): return (float(g_), float(g_))
        return (float(g_[0]), float(g_[-1]))
    GAP_ = np.array([_gap((s_.get("gap") or (s_.get("timing") or {}).get("gap_years")) if s_.get("tier") == "life event" or s_.get("per_year") else None)
                     for s_ in L.get("src", [{}] * L["S"])], float).reshape(-1, 2)   # build.py keeps it as timing gap_years
    if P["ev_gapfit"]:   # F9.13: a gap the Library's entry leaves out, fitted to Release's rows (a child version counts as one)
        rnm_ = np.asarray(L["names"], dtype=object)[np.asarray(L.get("ROOT", np.arange(L["S"])))]
        for nm_, g_ in P["ev_gapfit"].items():
            GAP_[rnm_ == nm_] = (float(g_[0]), float(g_[-1]))
    GAPM_ = ~np.isnan(GAP_[:, 0]); GAPON_ = bool(P["ev_gap"] and GAPM_.any())
    # far_ties (item 18): a far moment (cast_want: far_*) comes only with a tie's call, never by the everyday draw
    FARS_ = np.zeros(L["S"], bool)
    if "W_WANT" in L:
        import world_keys as WK_
        FARS_ = np.isin(np.asarray(L["W_WANT"]), [i_ for i_, w_ in enumerate(WK_.CAST_WANTS) if w_.startswith("far_")])
    FARS_ON_ = bool(FARS_.any())
    # lead_ways (S7): a post's moment (cast_want: lead_*) comes only with the post (taking it, a crisis, its fall, the
    # turn to routine, handing it on), never by the everyday draw of life events
    LEADS_ = np.zeros(L["S"], bool)
    if "W_WANT" in L:
        LEADS_ = np.isin(np.asarray(L["W_WANT"]), [i_ for i_, w_ in enumerate(WK_.CAST_WANTS) if w_.startswith("lead_")])
    LEADS_ON_ = bool(LEADS_.any())
    # S5, sacred lines: an offer, tragic trade-off or amends moment (cast_want: sacred, tragic, amends) comes only when the
    # life's own line brings it (WorldLink), never by the everyday draw or a yearly rate; the switch turns the lines on
    SACS_ = np.zeros(L["S"], bool)
    if "W_WANT" in L:
        SACS_ = np.isin(np.asarray(L["W_WANT"]), [i_ for i_, w_ in enumerate(WK_.CAST_WANTS) if w_ in WK_.OWN_WANTS])
    SACS_ON_ = bool(SACS_.any())
    SAC_ON_ = False                                       # (set with the world: its People has the lines)
    REG_ = REG_ & ~FARS_ & ~LEADS_ & ~SACS_   # (nor by the neighbouring stages' fill or the routine's; the Library's find, 10-10)
    # place_turnover (finishing pack, part 2): "the place closed" and "the new place" (cast_want: place_closed,
    # place_opened) come only with a closing or an opening of the life's place (WorldLink), never by a draw
    PTW_ = np.zeros(L["S"], bool)
    if "W_WANT" in L:
        PTW_ = np.isin(np.asarray(L["W_WANT"]), [i_ for i_, w_ in enumerate(WK_.CAST_WANTS) if w_ in getattr(WK_, "PLACE_WANTS", ())])
    PTW_ON_ = bool(PTW_.any())
    if PTW_ON_:
        REG_ = REG_ & ~PTW_
    # S3, S4 (sph_eyes, sph_odd): a caught-between or odd-one-out moment (cast_want: caught, odd) comes only when the place
    # reading brings it, never by the everyday draw
    EYEW_ = np.zeros(L["S"], bool)
    if "W_WANT" in L:
        EYEW_ = np.isin(np.asarray(L["W_WANT"]), [i_ for i_, w_ in enumerate(WK_.CAST_WANTS) if w_ in ("caught", "odd")])
    EYEW_ON_ = bool(EYEW_.any())
    if EYEW_ON_:
        REG_ = REG_ & ~EYEW_   # (nor by the stages' fill or the routine's, as far moments)
    # spheres finishing pack, part 4: a moment with a fellow inmate (cast_want: fellow_inmate) is open only while the life
    # holds an active former-inmate tie (the closest takes its first who: slot; world_link.who)
    INMS_ = np.zeros(L["S"], bool)
    if "W_WANT" in L and "fellow_inmate" in WK_.CAST_WANTS:
        INMS_ = np.asarray(L["W_WANT"]) == WK_.CAST_WANTS.index("fellow_inmate")
    INMS_ON_ = bool(INMS_.any())
    GAPLO_ = np.nan_to_num(GAP_[:, 0])[None]; GAPW_ = np.maximum(np.nan_to_num(GAP_[:, 1] - GAP_[:, 0]), 1 / 52)[None]
    # the same gap on an everyday or inner moment (a stray dog that follows you home is not a weekly thing): its weight ramps
    # from 0 at lo years after it last came to full at hi (the game thread's finding, 2026-10-05 22:00)
    GAPX_ = np.array([_gap((s_.get("gap") or (s_.get("timing") or {}).get("gap_years")) if s_.get("tier") in ("everyday", "inner") else None)
                      for s_ in L.get("src", [{}] * L["S"])], float).reshape(-1, 2)
    GAPXM_ = ~np.isnan(GAPX_[:, 0]); GAPXON_ = bool(P["ev_gap"] and GAPXM_.any())
    GAPXLO_ = np.nan_to_num(GAPX_[:, 0])[None]; GAPXW_ = np.maximum(np.nan_to_num(GAPX_[:, 1] - GAPX_[:, 0]), 1 / 52)[None]
    GAPM_I, GAPN_I, GAPX_I = np.nonzero(GAPM_)[0], np.nonzero(~GAPM_)[0], np.nonzero(GAPXM_)[0]   # speed pass: their columns
    ROUT_ = REG_ & ~(GAPXM_ & (GAPXLO_[0] > 0))   # gap_keep's routine: ordinary everyday moments whose gap starts at 0 (or none);
    # a moment whose gap starts later is an event in someone's life, and keeps its own rate and spacing (Library 07:27)
    FAMILY = L.get("FAMILY", {})                                           # an original's name -> it and its child versions
    alive = np.zeros((N, len(ROLES)))                     # parents, siblings, a closest friend, grandparents, partner, children
    kid_last = np.full(N, -10 ** 7)                        # the week the last child was born (R15: a baby's first year)
    kid_on = np.zeros(N, bool)                             # children held at the start of this week (counted already)
    # identity (point 11): sex from setup, attraction and unease drawn at birth and hidden
    sx_ = P["sex"]; rid = np.random.default_rng([int(seed), 11])   # its own random stream: the rest of the run is unchanged
    ID2 = bool(P["id_v2"])
    sxl_ = None if sx_ is None else [str(x).lower() for x in (sx_ if isinstance(sx_, (list, tuple, np.ndarray)) else [sx_] * N)]
    female = (rid.random(N) < (P["female_p"] if ID2 else 0.5)) if sx_ is None else np.array([x.startswith("f") for x in sxl_])
    attr = np.where(female, rid.choice(5, N, p=P["attr_p"][0]), rid.choice(5, N, p=P["attr_p"][1]))
    if ID2:   # N1b: own gender from the uniform that drew unease, so everyone who had unease keeps it; new draws go last
        ug_ = rid.random(N)
        gender_self = np.where(ug_ < P["trans_p"], 1, np.where(ug_ < P["trans_p"] + P["nb_p"], 2, 0))
        unease = gender_self > 0
        intersex = (rid.random(N) < P["intersex_p"]) if sx_ is None else np.array([x.startswith("i") for x in sxl_])
        raised_ = rid.random(N) < 0.5; attr_ix_ = np.where(raised_, rid.choice(5, N, p=P["attr_p"][0]), rid.choice(5, N, p=P["attr_p"][1]))
        female = np.where(intersex, raised_, female); attr = np.where(intersex, attr_ix_, attr)   # female: raised as
        ace = rid.random(N) < P["ace_p"]
        idr_ = np.random.default_rng([int(seed), 78])   # later identity draws (attraction drift, a partner's sex): own stream
        ps_u = idr_.random((N, 12))                     # one draw per partner, in order, whatever else the life does
        ps_n = np.zeros(N, int); partner_same = np.zeros(N, bool); par_prev = np.zeros(N, bool)
        named_g = np.zeros(N, bool); came_o = np.zeros(N, bool)      # own gender named; attraction told
        found_id = np.full((N, 4), NEVER)               # the week a moment gated on gender, attraction, ace, intersex first came
        rfit_avg = np.zeros(N); cross_title = np.zeros(N, bool); act_cw = np.zeros(N)
        setting_ = L.get("SETTING", "earth") if BAT else "earth"
        RS0 = P["role_strict"] if P["role_strict"] is not None else ROLE_BY_SETTING.get(setting_, 0.3)
        AT0 = P["accept_trans"] if P["accept_trans"] is not None else ACCEPT_BY_SETTING.get(setting_, 0.5)
    else:
        unease = rid.random(N) < P["unease_p"]
        gender_self = unease.astype(int); intersex = np.zeros(N, bool); ace = np.zeros(N, bool)
    dead = np.zeros(N, bool); died = []                   # the character's own death (self_death)
    pris_out = np.full(N, NEVER)                           # when a prison term ends ([ex-prisoner])
    pris_in = np.full(N, NEVER)                            # when it began (prison_ties: the years inside)
    if BAT:
        alive[:, 0] = 2; alive[:, 1] = rng.choice(4, N, p=[0.2, 0.4, 0.25, 0.15]); alive[:, 2] = 1; alive[:, 3] = rng.integers(2, 5, N)
    # birth order (checklist N4): which of the siblings are older; drawn from its own stream so no other draw moves
    older_sib = np.floor(np.random.default_rng([seed, 77]).random(N) * (alive[:, 1] + 1)).astype(int)
    younger_sib = alive[:, 1].astype(int) - older_sib
    friend_back = np.full(N, NEVER)
    AGO = ("le", "commit", "move", "death", "loss", "win", "hard_win", "fail_big", "breakup", "retire", "child", "job", "goal_end", "hard",
           "near_death", "fail_body", "fail_long")   # fail_body: a failed act that risked the body (body:, or death_if_fails)
    # (packs 07:52); fail_long: a failed long shot, an act for a title (or granting the long-shot perk) at true odds under
    # long_shot (packs 08:02)
    ago = {k_: np.full(N, NEVER) for k_ in AGO}           # the week each of these last happened
    STREAKS = ("quiet", "lo_meaning", "vlo_meaning", "lo_belong", "lo_peace", "hi_stress", "lo_time", "lo_auto", "ok_needs",
               "ok_body", "easing", "flat_comp")
    streak = {k_: np.zeros(N) for k_ in STREAKS}           # weeks in a row
    hist_m = np.full((N, C), 0.2); hist_e = np.full((N, C), 0.2)   # ten-year shares of the ways acted and the ends served
    hedon_n = np.zeros(N); bodyhab_n = np.zeros(N); fails13 = np.zeros(N); n_moves = np.zeros(N); heavy_risk = np.zeros(N)
    bind_m = np.zeros(N); bind_c = np.full((N, C), 0.2); end_t = np.full((N, NK), NEVER); widowed = np.zeros(N, bool)
    WHY = ["left", "lost job", "broke up", "widowed", "retired"]; end_why = np.full((N, NK), -1)
    comp_ref = np.full(N, 0.6); stress_slow = np.zeros(N); read_log = []; mark_log = []
    cond_ok = np.ones((N, L["S"]), bool); cond_fac = np.ones((N, L["S"])); cond_hold = np.zeros((N, L["S"])); cond_n = np.zeros(N)
    drv_sum = np.zeros(L["S"]); drv_cnt = np.zeros(L["S"])
    earn_sum = np.zeros(L["S"]); earn_cnt = np.zeros(L["S"])   # the earned lift of those who meet a title-giving moment
    ref_sum = np.zeros((L["S"], C)); ref_cnt = np.zeros(L["S"]); pk_sum = np.zeros((L["S"], L["K"])); pk_cnt = np.zeros((L["S"], L["K"]))   # chance
    WID_ON = JOBLOSS_ON = REJOB_ON = True; EV_KEEP = np.ones(len(EV["names"])); ECH = []; EVR = []
    if BAT:
        GATED = np.zeros(L["S"], bool); GATED[[c_["s"] for c_ in L["COND"]]] = True
        cond_ok[:, GATED] = False
        ECH = [c_ for c_ in L["COND"] if c_["kind"] == 2]; ECH_S = np.array([c_["s"] for c_ in ECH], int)
        ECH_R = RATE[ECH_S] / 0.3          # an echo's rate: (default .3) scales the share of its anchors that come back
        echo_anchor = np.full((N, len(ECH)), NEVER); echo_due = np.full((N, len(ECH)), NEVER); echo_end = np.full((N, len(ECH)), NEVER)
        echo_ready = np.zeros((N, len(ECH)), bool); echo_fac = np.ones((N, len(ECH)))
        EVR = L["EVR"]
        evr_next = np.stack([(max(e_["window"][0], 3) + rng.uniform(0, e_["gap"][1], N)) * 52 for e_ in EVR], 1) if EVR else np.zeros((N, 0))
        KILLS, ENDS, ONCE, ONCE_K = L["KILLS"], L["ENDS"], L["ONCE"], L["ONCE_K"]
        WID_ON = not (KILLS == ROLES.index("partner")).any()      # the batch's own "your partner dies" replaces built-in widowhood
        JOBLOSS_ON = not (ENDS == CAR).any()                      # and its "losing your job" the built-in job loss
        REJOB_ON = L.get("REJOB", -1) < 0                         # and its "a new job at last" the quiet return to work
        EV_KEEP = np.array([nm_ not in EV_DROP for nm_ in EV["names"]], float)
        KL_ = KILLS >= 0; INNER_ = L["INNER"]; KCH_ = KILLS[KL_] == ROLES.index("child")
    EP_ON = bool(P["echo_play"]) and BAT   # picks come back (see DEFAULT's echo_play)
    ep_seeds = []; ep_now = np.full(N, -1); ech_now = np.full(N, -1)   # the seeds; the seed (index) whose return is this week's
    if EP_ON:
        EPP = P["echo_play_par"]; ep_rng = np.random.default_rng([int(seed), 2917]); ep_last = np.full(N, -10 ** 6)
        EP_C = {}   # (kind, went well) -> [(moment, echo index or -1, its condition)]: the return moments by of: and side:,
        for e_, c_ in enumerate(ECH):   # and the mark echoes by the kind their anchor names (mk_ok: only one that went well)
            for ok_k in (True, False):
                k_ = re.match(r"\s*mk(_ok)?\(\s*['\"]([^'\"]+)['\"]", c_.get("atxt", ""))
                if k_ and (ok_k or not k_.group(1)):
                    EP_C.setdefault((k_.group(2), ok_k), []).append((c_["s"], e_, c_))
        for c_ in L["COND"]:
            if c_["kind"] == 4 and c_.get("of"):
                for ok_k in ((True,) if c_.get("side") == "well" else (False,) if c_.get("side") == "badly" else (True, False)):
                    EP_C.setdefault((c_["of"], ok_k), []).append((c_["s"], -1, c_))

    BO_ON = bool(P["bold_play"]) and BAT and bool(L.get("BOLD"))   # bold ways (see DEFAULT's bold_play)
    bold_now = None; bold_pick = np.full(N, -1)   # this week's bold slots (asked weeks) and the slot taken (-1: none)
    if BO_ON:
        BO_ROWS, BO_S = L["BOLD"], L["BOLD_S"]
        bo_row = np.full((N, 2), -1); bo_base = np.full((N, 2), -1); bo_ph = np.zeros((N, 2))   # each slot's row, base way, felt odds
        bo_kp = np.ones((N, 2))   # and the chance its win is kept (F16), as the card counts it
        bo_n = np.zeros(N, int); bo_seed = np.full(N, -1); bo_title = [None] * N   # seeds planted; this week's; its title
        bold_log = []   # (life, week, row, slot, odds, worked)
        def bo_odds(n, rw_, p0_):
            """A bold way's odds for life n from its base way's (p0_): the written chances' logit gap, then likelier_if:
            points, between .1 and .9."""
            p0_ = min(max(float(p0_), 1e-6), 1 - 1e-6)
            p_ = 1 / (1 + np.exp(-(np.log(p0_ / (1 - p0_)) + rw_["shift"])))
            for op_, j_, y_, pts_ in rw_["lik"]:
                if op_ == "mark":
                    h_ = mark_n[n, j_] > 0
                else:
                    h_ = RON and r_has[n, j_] and (op_ == "has" or t - r_since[n, j_] >= y_ * 52)
                p_ += pts_ / 100 * bool(h_)
            return min(max(p_, 0.1), 0.9)
        def bo_live(n, rw_):
            """Whether a bold way's win and cost would both change something for life n: each title or perk it gives
            not held yet, each it drops, takes or suspends held (else the card would state what cannot happen)."""
            if not RON:
                return True
            for w_ in ("ok", "fail"):
                for op_, j0_, _ in rw_["fx"][w_]:
                    js_ = fx_targets(n, rw_["s"], j0_)
                    if not js_ or (any(r_has[n, j_] for j_ in js_) if op_ in ("title", "grants") else not any(r_has[n, j_] for j_ in js_)):
                        return False
            return True
        def bo_keep(n, rw_):
            """The chance a bold way's win is kept for life n: each title it gives that would start a partnership, children
            or a faith not held leans as F16 has it (r_gain refuses it otherwise); 1 for any other win. The card's odds
            count it; the act's own odds do not."""
            if not (CRS_ON and RON):
                return 1.0
            k_ = 1.0
            for op_, j0_, _ in rw_["fx"]["ok"]:
                if op_ not in ("title", "grants"):
                    continue
                for i_ in fx_targets(n, rw_["s"], j0_):
                    if i_ < NT_ and TK_[i_] < NK and CRS_J[TK_[i_]] >= 0 and not held[n, TK_[i_]]:
                        j_ = CRS_J[TK_[i_]]
                        k_ *= min(float(np.exp(CRS_MU[j_] + crs_own[n, j_] + (5 * w[n] - 1) @ CRS_T[j_])), 1.0)
            return k_
    # ---- footprints (foot_on; chroma-ideas/next-table-2026-10-19/plan.md section 3): what a picked option visibly
    # leaves (the Library's FOOT tables, batch L["FOOT"]), given real state. A person: with the world on, the closest of
    # that role in the cast grows closer or someone new comes in that role (lost: the closest drifts); off-world, ties
    # move by foot_par ties. A place: that haunt kind joins the life's haunts (the world on, its haunts built). A means:
    # the resource moves by the amount. A mark or a door: the mark is left as an option's mark: is (a door opens through
    # the echoes and back: links that read it). A lesson: told only (the act's own colour lesson is already learned).
    # Means, marks, doors, lessons and a person lost come on any try; a person met and a place joined only when it works
    # (as a haunt choice). An option's own mark counts as a mark footprint when a rule reads it (L["FOOT_OWN"]), in the
    # moments footprints are for (L["FOOT_S"]: the life events and those with FOOT tables, not the everyday). Only what
    # lands is kept. foot_log: one record per pick with footprints (life, age, moment, label, worked, feet). For the game,
    # per life: foot[n], what the life's last act left, as (kind, value, who: the cast id for a person, else -1); foot_open[n],
    # the doors still waiting, as (kind, since t), each shut when a moment reading it is met (L["FOOT_READS"])
    FOOT_ON = bool(P["foot_on"]) and bool(L.get("FOOT"))
    foot_log = []
    foot = [[] for _ in range(N)] if FOOT_ON else None
    foot_open = [[] for _ in range(N)] if FOOT_ON else None
    FT_HAS = FT_OWN = None
    if FOOT_ON:
        FT_HAS = np.zeros((L["S"], L["K"]), bool)
        for (s_, k_) in L["FOOT"]:
            FT_HAS[s_, k_] = True
        FT_OWN = np.isin(np.array(L["MARKS"], object), L["FOOT_OWN"])
        # a door only a return reads (none in the batch, or a return of its kind) shuts after foot_par door_yrs, or with
        # picks coming back (echo_play) after the seed's keep (Library 10-19)
        FT_DOOR = 52 * (P["echo_play_par"]["keep"] if EP_ON else P["foot_par"]["door_yrs"])
    def foot_apply(live_, hm_, mk_):
        """This week's acts leave their footprints (FOOT_ON); hm_: the lives whose act left its own mark, mk_ (the mark)."""
        for n in np.nonzero(live_)[0]:   # a door shuts when a moment reading its mark is met
            if foot_open[n]:
                foot_open[n] = [d_ for d_ in foot_open[n] if d_[0] not in MIDX or not (L["FOOT_READS"][s[n], MIDX[d_[0]]]
                                or (L["FOOT_RET"][MIDX[d_[0]]] and t - d_[1] >= FT_DOOR))]
        fto_ = set(int(n) for n in hm_ if FT_OWN[mk_[n]] and L["FOOT_S"][s[n]])
        for n in np.nonzero(live_ & ~idle)[0]:
            ok_ = bool(succ[n]); feet_ = []; foot[n] = []
            for kd_, x_, y_, val_ in (L["FOOT"][(int(s[n]), int(a[n]))] if FT_HAS[s[n], min(a[n], L["K"] - 1)] else ()):
                rec_ = dict(kind=L["FOOT_KINDS"][kd_], value=val_); who_ = -1
                if kd_ == 0:   # a person
                    if not (ok_ or y_):
                        continue
                    if WON:
                        r_ = WL.PP.foot_person(int(n), val_.partition(" ")[0], lost=bool(y_), colour=ma[n])
                        if r_ is None:
                            continue
                        rec_.update(cid=r_["cid"], new=r_["new"]); who_ = int(r_["cid"])
                    else:
                        res[n, TIE] = min(1.0, max(0.0, res[n, TIE] + (-1 if y_ else 1) * P["foot_par"]["ties"]))
                elif kd_ == 1:   # a place
                    if not ok_:
                        continue
                    if WON:
                        p_ = WL.PP.pick_haunt(int(n), val_.split(".")[0], int(np.argmax(ma[n])), kind=x_)
                        if p_ < 0:
                            continue
                        rec_["place"] = int(p_)
                elif kd_ == 2:   # a means (moved: what it moved, clipped at 0 and 1)
                    r0_ = res[n, x_]; res[n, x_] = min(1.0, max(0.0, r0_ + y_)); rec_["moved"] = round(float(res[n, x_] - r0_), 4)
                elif kd_ in (3, 4):   # a mark or a door (once a week)
                    if x_ < 0:
                        continue
                    if mark_last[n, x_] != t:
                        if mark_n[n, x_] == 0:
                            mark_first[n, x_] = t
                        mark_last[n, x_] = t; mark_ok[n, x_] = ok_; mark_n[n, x_] += 1
                        mark_log.append((int(n), t, int(x_), ok_))
                        if n in events:
                            events[n].append(dict(mark=dict(age=round(age, 2), mark=L["MARKS"][x_], worked=ok_)))
                    if kd_ == 4 and all(d_[0] != val_ for d_ in foot_open[n]):
                        foot_open[n].append((val_, t))
                    if mk_[n] == x_:   # the act's own mark, named here already
                        fto_.discard(int(n))
                feet_.append(rec_); foot[n].append((rec_["kind"], val_, who_))
            if int(n) in fto_:   # the act's own mark, when a rule reads it
                rec_ = dict(kind="mark", value=L["MARKS"][mk_[n]], own=True)
                feet_.append(rec_); foot[n].append(("mark", rec_["value"], -1))
            if feet_:
                fr_ = dict(life=int(n), age=round(t / 52, 2), moment=L["names"][s[n]], label=L["labels"][s[n]][a[n]],
                           worked=ok_, feet=feet_)
                foot_log.append(fr_)
                if n in events:
                    events[n].append(dict(foot=fr_))
