# run_05_conditions.py: part 5 of 18 of engine._run, the life loop.
# The condition reading (cond_ns, rw_clause, ev_cond, factor), sources, seasons, shares, kills, roles by sex.
# Lines here are _run's own, unchanged and at their own indent: engine.py joins the parts in order (engine.RUN_PARTS)
# and compiles them as one, so a name used here may be set in an earlier part. Never import or run it alone.
    def cond_ns(t, age, w):
        """The engine's condition vocabulary (batch.COND_VOCAB): one value per person."""
        def ys(x):
            return np.where(x <= NEVER // 2, 99.0, (t - x) / 52.0)
        def mk(name, yrs=None):
            j_ = MIDX[name]; ok_ = mark_last[:, j_] > NEVER // 2
            return ok_ if yrs is None else ok_ & ((t - mark_last[:, j_]) <= np.asarray(yrs) * 52 + 1e-9)
        def had(names_, yrs):
            key_ = tuple(names_); idx_ = HAD_IDX.get(key_)   # speed pass: each list of names resolved once
            if idx_ is None:
                idx_ = HAD_IDX[key_] = [i_ for n_ in names_ for i_ in FAMILY.get(n_, [SIDX[n_]] if n_ in SIDX else [])]
            return ((t - sit_last[:, idx_]) <= yrs * 52).any(1) if idx_ else np.zeros(N, bool)
        ns = dict(abs=np.abs, mk=mk, mk_ok=lambda name, yrs=None: mk(name, yrs) & mark_ok[:, MIDX[name]],
                  mkn=lambda name: mark_n[:, MIDX[name]], mk_span=lambda name: ys(mark_first[:, MIDX[name]]) * (mark_n[:, MIDX[name]] > 0),
                  had=had, chance=lambda p: rng.random(N) < p,
                  age=age, age_mod=int(age) % 10, decade_edge=int(age) % 10 in (9, 0), round_birthday=int(age) % 10 == 0, stage=stage,
                  stress=stress, mood=mood, satisfaction=content, peace=peace, react=react, steady=steady, base_mood=base_mood,
                  outlook=outlook, support=support, wound=wound, trouble=trouble, fortune=fortune, cload=cload,
                  yrs_any=np.where(held, (t - since) / 52, 0).max(1), kids_home=kids, retired=retired, widowed=widowed,
                  fails13=fails13, hedon_n=hedon_n, bodyhab_n=bodyhab_n, n_moves=n_moves, heavy_risk=heavy_risk, bind_m=bind_m,
                  n_dream=(gk == 0).sum(1), n_passion=(gk == 1).sum(1), n_plan=(gk == 2).sum(1),
                  regret=regret, horizon=fhz, discipline=dsc, self_control=ctrl,     # v7: what was let go, time felt short, learned control
                  harsh=drv_h, unrest=drv_u, prosper=drv_p, era=era_i[t],
                  founding=(WL.W.c5_founding(WL.PP.loc) if WL is not None and P.get("c5_faith") else NO_FOUND),   # C5: a
                  # movement founded in the person's town within the year (the founding took a free slot)
                  haunts=np.full(N, bool(P.get("sph_haunts")) and WON))   # spheres phase 2: haunts built (the haunt choices)
        ns.update({nm_: stage == i_ for i_, nm_ in enumerate(STAGE_NAMES)})
        ns.update({nm_: need[:, i_] for i_, nm_ in enumerate(NEEDS)}); ns.update({nm_: res[:, i_] for i_, nm_ in enumerate(RESOURCES)})
        for i_, c_ in enumerate(COLORS):
            ns[c_] = w[:, i_]; ns["h" + c_] = hist_m[:, i_]; ns["e" + c_] = hist_e[:, i_]
        for i_, k_ in enumerate(KNAMES):
            ns["held_" + k_] = held[:, i_]; ns["yrs_" + k_] = np.where(held[:, i_], (t - since[:, i_]) / 52, 0.0)
            ns["ago_end_" + k_] = ys(end_t[:, i_])
        for i_, r_ in enumerate(ROLES[:4]):
            ns["alive_" + r_] = alive[:, i_]
        ns["alive_child"] = alive[:, 5]                    # R15: living children (a child's death leaves the others)
        ns["kid_young"] = np.where(held[:, KID] & (kid_last > NEVER // 2), (t - kid_last) / 52, 99.0)   # F7: the youngest's years
        ns["older_siblings"] = older_sib; ns["younger_siblings"] = younger_sib   # birth order (N4)
        for k_ in AGO:
            ns["ago_" + k_] = ys(ago[k_])
        ns.update(streak)
        ns["inmate_tie"] = pt_act.copy(); ns["yrs_out"] = ys(pt_rel)   # part 4: an active former-inmate tie; years out
        ns["married"] = held[:, PAR] & (sit_last[:, SIDX["getting married"]] >= since[:, PAR]) if "getting married" in SIDX else np.zeros(N, bool)
        ns.update(female=female, male=~female, attr=attr, unease=unease)   # identity (point 11): sex, attraction 0-4, unease
        if ID2:   # N1b (chroma-identity/for-the-engine.md §2)
            rs_v, at_v, _ = role_view()
            ns.update(trans=gender_self == 1, nonbinary=gender_self == 2, ace=ace, intersex=intersex, partner_same=partner_same,
                      named_gender=named_g, cross_title=cross_title, role_fit=1 - rfit_avg, role_strict=rs_v, accept_trans=at_v)
        else:
            ns.update(trans=unease, nonbinary=np.zeros(N, bool), ace=ace, intersex=intersex, partner_same=np.zeros(N, bool),
                      named_gender=np.zeros(N, bool), cross_title=np.zeros(N, bool), role_fit=np.ones(N),
                      role_strict=np.zeros(N), accept_trans=np.full(N, 0.5))
        if RON:   # titles and perks: has('nurse'), was('soldier'), yrs_has('homeowner')
            ns["has"] = lambda nm: r_has[:, RID[nm]]; ns["was"] = lambda nm: r_ever[:, RID[nm]]
            ns["yrs_has"] = lambda nm: np.where(r_has[:, RID[nm]], (t - r_since[:, RID[nm]]) / 52, 0.0)
            ns["n_titles"] = r_has[:, :NT_].sum(1); ns["n_perks"] = r_has[:, NT_:].sum(1)
        else:
            ns["has"] = ns["was"] = lambda nm: np.zeros(N, bool); ns["yrs_has"] = lambda nm: np.zeros(N)
            ns["n_titles"] = ns["n_perks"] = np.zeros(N)
        ns["betrayed"] = had(["a partner's affair comes to light", "betrayed by a friend or a business partner"], 10)
        # stage 2 (Library's for-the-engine-stage2.md): a colour's rise over some years, how long it (or a pair) has held
        # above a share (quarterly, up to ten years), and the shadow's force, part, seen and years since its reflection
        def q_back(yrs):
            return w_q[(w_qi - 1 - int(round(4 * yrs))) % 40] if w_qi > int(round(4 * yrs)) else np.full((N, C), 0.2)
        def q_run(ok_):   # ok_ (40 quarters newest first, N): the quarters in a row, from the newest, that hold, in years
            return np.cumprod(ok_, 0).sum(0) / 4.0
        def q_new():
            return w_q[(w_qi - 1 - np.arange(min(w_qi, 40))) % 40]
        def first_age(names_):   # the age a moment (or any of a list) was first met, 99 if never
            idx_ = [i_ for n_ in names_ for i_ in FAMILY.get(n_, [SIDX[n_]] if n_ in SIDX else [])]
            if not idx_:
                return np.full(N, 99.0)
            f_ = np.where(sit_first[:, idx_] <= NEVER // 2, 10 ** 9, sit_first[:, idx_]).min(1)
            return np.where(f_ >= 10 ** 9, 99.0, f_ / 52.0)
        ns.update(first_age=first_age, rise=lambda c, yrs=2: w[:, IDX[c]] - q_back(yrs)[:, IDX[c]],
                  above_yrs=lambda c, th: q_run(q_new()[:, :, IDX[c]] > th),
                  pair_yrs=lambda c1, c2, th: q_run((q_new()[:, :, IDX[c1]] > th) & (q_new()[:, :, IDX[c2]] > th)),
                  sh=lambda c: shA[:, IDX[c]], sh_part=lambda c: shS[:, IDX[c]], sh_seen=lambda c: sh_seen[:, IDX[c]],
                  sh_ago=lambda c: ys(sh_rt[:, IDX[c]]))
        ns["adj"] = lambda nm: adj[:, ADJ_ID[nm]]                       # v7 adjectives: adj('wealthy'), is_wealthy
        ns["yrs_adj"] = lambda nm: np.where(adj[:, ADJ_ID[nm]], (t - adj_since[:, ADJ_ID[nm]]) / 52, 0.0)
        ns.update({"is_" + nm_.replace(" ", "_"): adj[:, i_] for i_, nm_ in enumerate(ADJ_NAMES)})
        return ns
    RW_CODE = {}   # role_why: each clause's source, compiled once
    def rw_clause(src, ns, n, ext=()):
        """role_why: what in a rule's condition (its source) held for life n this week, as a list of the history items
        behind it, or None if it does not hold. Read-only: chance() is never drawn (read as luck), & gives every part, |
        the first part that holds, ~ (an absence) nothing."""
        nsx = dict(ns, chance=lambda p_: np.ones(N, bool))
        def val(nd):
            k_ = ast.dump(nd)
            c_ = RW_CODE.get(k_)
            if c_ is None:
                c_ = RW_CODE[k_] = compile(ast.Expression(nd), "<why>", "eval")
            return bool(np.broadcast_to(np.asarray(eval(c_, EV_G, nsx)), (N,))[n])
        def item(nd):
            yrs_ = None
            for x in ast.walk(nd):
                if isinstance(x, ast.Call) and isinstance(x.func, ast.Name):
                    f_ = x.func.id
                    a0 = x.args[0].value if x.args and isinstance(x.args[0], ast.Constant) else None
                    if len(x.args) > 1 and isinstance(x.args[1], ast.Constant):
                        yrs_ = x.args[1].value
                    if f_ in ("mk", "mk_ok", "mkn", "mk_span") and a0 in MIDX:
                        j_ = MIDX[a0]; tm_ = int(mark_last[n, j_]); src_ = rw_mk.get((n, j_))
                        it_ = dict(k="mark", mark=a0, t=tm_)
                        if src_ is not None and src_[0] == tm_:
                            it_.update(moment=L["names"][src_[1]], s=src_[1], a=src_[2])
                        return it_, yrs_
                    if f_ in ("had", "first_age") and x.args and isinstance(x.args[0], (ast.List, ast.Tuple)):
                        nm_ = [e_.value for e_ in x.args[0].elts if isinstance(e_, ast.Constant)]
                        idx_ = [i_ for n_ in nm_ for i_ in FAMILY.get(n_, [SIDX[n_]] if n_ in SIDX else [])]
                        if idx_:
                            tl_ = sit_last[n, idx_] if f_ == "had" else np.where(sit_first[n, idx_] <= NEVER // 2, 10 ** 9, sit_first[n, idx_])
                            b_ = idx_[int(np.argmax(tl_) if f_ == "had" else np.argmin(tl_))]
                            return dict(k="moment", name=L["names"][b_], s=int(b_),
                                        t=int(sit_last[n, b_] if f_ == "had" else sit_first[n, b_])), yrs_
                    if f_ in ("has", "was", "yrs_has") and a0 in RID:
                        return dict(k="held", name=a0, t=int(r_since[n, RID[a0]])), None
                    if f_ in ("adj", "yrs_adj"):
                        return dict(k="standing", name=a0), None
                    if f_ == "chance":
                        return dict(k="luck"), None
                    return dict(k="state", name=f_ if a0 is None else f_ + " " + str(a0)), None
            for x in ast.walk(nd):
                if isinstance(x, ast.Name):
                    nm_ = x.id
                    if nm_ == "money":
                        return dict(k="money"), None
                    if nm_ in RESOURCES:
                        return dict(k="means", name=nm_), None
                    if nm_ in NEEDS:
                        return dict(k="need", name=nm_), None
                    if nm_ in COLORS:
                        return dict(k="colour", name=nm_), None
                    if nm_ == "stage" or nm_ in STAGE_NAMES:
                        return dict(k="stage", name=nm_), None
                    if nm_ in ("age", "age_mod", "decade_edge", "round_birthday"):
                        return dict(k="age"), None
                    if nm_.startswith(("held_", "yrs_")) and nm_.split("_", 1)[1] in KNAMES:   # a commitment held, since
                        k_ = KNAMES.index(nm_.split("_", 1)[1])
                        return dict(k="held", name=KNAMES[k_], t=int(since[n, k_])), None
                    if nm_.startswith("ago_"):
                        return dict(k="since", name=nm_[4:]), None
                    if nm_.startswith("is_"):
                        return dict(k="standing", name=nm_[3:].replace("_", " ")), None
                    return dict(k="state", name=nm_), None
            return dict(k="state"), None
        def walk(nd):
            if isinstance(nd, ast.BinOp) and isinstance(nd.op, ast.BitAnd):
                return walk(nd.left) + walk(nd.right)
            if isinstance(nd, ast.BinOp) and isinstance(nd.op, ast.BitOr):
                b_ = nd.left if val(nd.left) else nd.right
                pk_ = ext_.get(ast.dump(b_), False)
                return ([dict(k="pack", pack=pk_, clause=ast.unparse(b_))] if pk_ is not False else []) + walk(b_)
            if isinstance(nd, ast.UnaryOp) and isinstance(nd.op, (ast.Invert, ast.Not)):
                return []
            it_, yrs_ = item(nd)
            it_["clause"] = ast.unparse(nd)
            if yrs_ is not None:
                it_["within"] = yrs_
            return [it_]
        if not src:
            return []
        ext_ = {ast.dump(ast.parse(x_, mode="eval").body): p_ for p_, x_ in ext}   # a pack's way in, or-ed into the rule
        body_ = ast.parse(src, mode="eval").body
        return walk(body_) if val(body_) else None
    def ev_cond(code, ns):
        r_ = eval(code, EV_G, ns)
        if type(r_) is np.ndarray and r_.shape == (N,):   # speed pass: the same copy, without broadcasting
            return r_.astype(bool)
        if isinstance(r_, (bool, np.bool_)):
            return np.ones(N, bool) if r_ else np.zeros(N, bool)
        return np.broadcast_to(np.asarray(r_), (N,)).astype(bool)
    def ev_memo(code, ns, memo):
        """Speed pass: ev_cond, reusing the answer of an equal condition already read with the same ns. Never for one
        that draws chance (a fresh draw each time) or reads sa (set per echo)."""
        if memo is None or "chance" in code.co_names or "sa" in code.co_names:
            return ev_cond(code, ns)
        r_ = memo.get(code)
        if r_ is None:
            r_ = memo[code] = ev_cond(code, ns)
        return r_
    def ep_return(s, s_ep):
        """Picks come back (echo_play): this week's return for each life. An ordinary echo drawn this week (ech_now) of a
        kind with a waiting seed a year old is the newest such seed's return; else the oldest due seed, at EPP w (no life
        event, no season step, gap years after the last), takes the week with one moment of its kind and side open to them:
        one never met first, else one not met for again years."""
        for n in np.nonzero(ech_now >= 0)[0]:
            if s[n] != s_ep[n]:
                continue
            for i_ in range(len(ep_seeds) - 1, -1, -1):
                sd_ = ep_seeds[i_]
                if sd_["n"] == n and sd_["done"] is None and t - sd_["t"] >= 52 \
                        and any(e_ == ech_now[n] for _, e_, _ in EP_C.get((sd_["kind"], sd_["ok"]), ())):
                    sd_["done"] = t; sd_["got"] = int(s[n]); ep_now[n] = i_; ep_last[n] = t
                    break
        for i_, sd_ in enumerate(ep_seeds):
            n = sd_["n"]
            if sd_["done"] is not None or sd_["due"] is None or t < sd_["due"] or ep_now[n] >= 0:
                continue
            if t > sd_["due"] + EPP["keep"] * 52:   # too long past: it stays a seed that never came back
                sd_["done"] = -1
                continue
            if had_ev[n] or dead[n] or s[n] != s_ep[n] or t - ep_last[n] < EPP["gap"] * 52 or ep_rng.random() >= EPP["w"]:
                continue
            ys_ = (t - sd_["t"]) / 52; sa0_ = ns.get("sa"); ns["sa"] = np.full(N, ys_)
            for k_ in (sd_["kind"], sd_.get("alt")):   # bold ways: a bold seed with no link of its own open takes a shared
                if k_ is None:                         # link of its kind of change (of_change:) and side
                    continue
                c_ = [(s_, e_) for s_, e_, cd_ in EP_C.get((k_, sd_["ok"]), ())
                      if avail0[n, s_] and not once_done[n, ROOT[s_]] and ys_ >= cd_["delay"][0] and ev_cond(cd_["req"], ns)[n]]
                new_ = [x for x in c_ if sit_n[n, x[0]] == 0] or [x for x in c_ if t - sit_last[n, x[0]] >= EPP["again"] * 52]
                if new_:
                    break
            ns["sa"] = sa0_
            if not new_:
                continue
            s_, e_ = new_[int(ep_rng.integers(len(new_)))]
            s[n] = s_; sd_["done"] = t; sd_["got"] = int(s_); ep_now[n] = i_; ep_last[n] = t
            if "bold" in sd_:   # a bold seed's link: shared or its own; gone when someone of its moment has died since
                sd_["link"] = True; sd_["change"] = k_ != sd_["kind"]
                if WON and sd_["who"]:
                    sd_["gone"] = any(((WL.PP.uid[n] == u_) & WL.PP.used[n] & ~WL.PP.lv[n]).any()
                                      for sl_, u_ in sd_["who"].items() if sl_ != "dead")
            if e_ >= 0:   # a mark echo: its own clock is spent
                echo_anchor[n, e_] = NEVER; echo_ready[n, e_] = False
    def factor(c_, ns, memo=None):
        f_ = np.ones(N)
        if not c_["more"] and not c_["less"]:   # speed pass: nothing to read, so 1 (as clip of ones gave)
            return f_
        for cd in c_["more"]:
            f_ = f_ * np.where(ev_memo(cd, ns, memo), P["cond_more"], 1.0)
        for cd in c_["less"]:
            f_ = f_ * np.where(ev_memo(cd, ns, memo), P["cond_less"], 1.0)
        return np.minimum(np.maximum(f_, 0.1), 6.0)   # speed pass: clip's own two steps, without its wrapper

    # threshold seasons (see season): which moments belong to which crossing, and each person's open season
    TH_K = np.full(L["S"], -1); TH_STEP = np.zeros(L["S"], int); TH_TR = np.zeros(L["S"], bool); TH_P = np.ones(L["S"])
    for si_, x_ in enumerate(L.get("src", []) if BAT else []):
        th_ = str(x_.get("threshold") or "").strip()
        if not th_:
            continue
        if th_.startswith("title:"):
            if not RON:
                continue
            if th_[6:].strip() not in GR["ID"]:
                raise ValueError(f"{L['names'][si_]}: threshold: {th_} names no title in the catalogue")
            TH_K[si_] = NS + GR["ID"][th_[6:].strip()]
        elif th_ in STAGE_NAMES:
            TH_K[si_] = STAGE_NAMES.index(th_)
        else:
            raise ValueError(f"{L['names'][si_]}: threshold: {th_} is neither a life stage {STAGE_NAMES} nor title:<name>")
        TH_STEP[si_] = int(x_.get("step") or 1)
        TH_TR[si_] = str(x_.get("transform") or "").strip().lower() in ("yes", "true", "1")
        if P["season_share"]:   # the share of lives its times: line gives ("perhaps 1 in 20", "about half"); else every season
            tm_ = str((x_.get("timing") or {}).get("times") or x_.get("times") or "").lower()
            m_ = re.search(r"\b1 in (\d+)", tm_)
            TH_P[si_] = 1.0 / float(m_.group(1)) if m_ else 0.5 if "half" in tm_ else 1.0
            if P["season_excl"]:   # K6: "1 homeowner in 20" counts too, and the words alone give a share
                m_ = re.search(r"\b1 (?:[a-z-]+ ){0,3}in (\d+)", tm_)
                h_ = [(m2_.start(), v_) for k_, v_ in P["season_words"] for m2_ in [re.search(r"\b" + k_, tm_)] if m2_]
                w_ = min(h_)[1] if h_ else 1.0   # the first such word in the line
                TH_P[si_] = 1.0 / float(m_.group(1)) if m_ else 0.5 if "half" in tm_ else w_
    SEA_ON = bool(P["season"]) and bool((TH_K >= 0).any())
    TH_ANY = TH_K >= 0; TH_TITLE = {int(k_ - NS) for k_ in TH_K[TH_K >= NS]}
    sea_k = np.full(N, -1); sea_t0 = np.zeros(N, int); sea_done = np.zeros((N, 4), bool); sea_log = []   # steps 1-3, transform
    sea_had = np.zeros((N, NS), bool)                     # a stage's season comes once in a life
    sea_rng = np.random.default_rng([int(seed), 79])       # season_share's draws, on their own stream
    ent_rng = np.random.default_rng([int(seed), 80])       # a first job's or a job move's title acceptance (acc_first, acc_move)
    far_rng = np.random.default_rng([int(seed), 81])       # whether one's own move is to a new town (far_share, E6)
    fam_rng = np.random.default_rng([int(seed), 84])       # whether the family's move is to a new town (move_near, K2)
    def _mv_far(x_):   # K2: moves: far / near from the Library; moves: yes is far when the moment names a new town
        v_ = str(x_.get("moves")).strip().lower()
        return 1.0 if v_ == "far" else 0.0 if v_ == "near" else 1.0 if "new town" in str(x_.get("name", "")) else P["fam_far"]
    MVF_ = np.array([_mv_far(x_) for x_ in L.get("src", [])] + [P["fam_far"]] * (L["S"] - len(L.get("src", []))))
    RETIRES_ = np.array([bool(x_.get("retires")) for x_ in L.get("src", [])] + [False] * (L["S"] - len(L.get("src", []))))
    ELD_ = STAGE_NAMES.index("elder")
    # retirement is the crossing into later life (the Library, 22:30): when the batch's elder season has a moment that
    # retires the person ('the last day at work'), retiring opens that season and its first step is the last day
    RET_SEA = SEA_ON and P["retire_season"] and bool((RETIRES_ & (TH_K == ELD_) & (TH_STEP == 1)).any())
    ret_pend = np.full(N, -1)
    # share: <0-1> on a moment (the Library, 23:50): the real share of people who ever meet it in life. Who they are is
    # drawn once, at birth (the person who goes fishing, runs a half marathon, volunteers at a shelter); the moment stays
    # closed to everyone else, and its once, gap and rate shape it for those it can come to
    SH_I = np.array([i_ for i_, x_ in enumerate(L.get("src", []) if BAT else []) if x_.get("share") is not None], int)
    SH_ON = len(SH_I) > 0
    if SH_ON:
        sh_v = np.array([float(L["src"][i_]["share"]) for i_ in SH_I])
        if ((sh_v <= 0) | (sh_v > 1)).any():
            raise ValueError(f"share: must be above 0 and at most 1 ({[L['names'][i_] for i_ in SH_I[(sh_v <= 0) | (sh_v > 1)]]})")
        if RON:   # the share is of all people: on a holds: moment, the draw among holders is share / the holders' share
            for j_, i_ in enumerate(SH_I):   # (the packs, 01:40: a door that needs holders reached only share x holders)
                if GR["S_HASHOLD"][i_]:
                    hsh_ = min(1.0, float(GR["share"][GR["S_HOLDM"][i_]].sum()))
                    sh_v[j_] = min(1.0, sh_v[j_] / hsh_) if hsh_ > 0 else sh_v[j_]
        SH_U = np.random.default_rng([int(seed), 17]).random((N, len(SH_I)))   # its own random stream
        grp_ = [str(L["src"][i_].get("share_group") or "").strip() for i_ in SH_I]
        for g_ in set(grp_) - {""}:   # share_group: one draw for the moments of a group (the two halves of a pair): with a
            jj_ = [j_ for j_, x_ in enumerate(grp_) if x_ == g_]   # common draw, those open to the rarer one are open to all
            SH_U[:, jj_] = SH_U[:, [jj_[0]]]
        SH_EL = SH_U < sh_v[None]
    SW_ = np.append(np.asarray(P["season_weeks"], int), int(P["season_tr_week"]))   # the weeks of steps 1-3 and the transform
    SEA_LEN_Y = P["season_len"] / 52
    # the ages a stage's season moments are written for: where their age windows meet, within the rite's own window
    SEA_LO = np.full(NS, np.nan); SEA_HI = np.full(NS, np.nan)
    for k_ in range(1, NS):
        m_ = TH_K == k_
        if SEA_ON and m_.any():
            lo_, hi_ = max(L["AGE"][m_, 0].max(), STAGE_LO[k_]), min(L["AGE"][m_, 1].min(), STAGE_HI[k_])
            if hi_ - lo_ < SEA_LEN_Y:   # the windows do not meet: the typical one
                lo_ = max(float(np.median(L["AGE"][m_, 0])), STAGE_LO[k_])
                hi_ = max(lo_ + SEA_LEN_Y, min(float(np.median(L["AGE"][m_, 1])), STAGE_HI[k_]))
            SEA_LO[k_], SEA_HI[k_] = lo_, hi_
    SEA_AGE_ON = SEA_ON and bool(P["season_by_age"]) and bool((~np.isnan(SEA_LO)).any())
    SEA_KS = [k_ for k_ in range(1, NS) if not np.isnan(SEA_LO[k_])]
    sea_age = (np.nan_to_num(SEA_LO)[None] + np.random.default_rng([int(seed), 13]).random((N, NS))
               * np.maximum(np.nan_to_num(SEA_HI - SEA_LO) - SEA_LEN_Y, 0)[None])   # its own random stream

    def sea_fits(k_, a_):   # a crossing at age a_ can open stage k_'s season (its moments can still be met)
        return not SEA_AGE_ON or k_ >= NS or np.isnan(SEA_LO[k_]) or (SEA_LO[k_] <= a_ <= SEA_HI[k_] - SEA_LEN_Y)

    # a wider world (point 11): the Library's death_if_fails: and kills: on options
    A_DEATH = np.zeros((L["S"], L["K"])); A_KILL = np.full((L["S"], L["K"]), -1)   # -2: someone the engine does not track
    A_KILLF = np.full((L["S"], L["K"]), -1); A_KILLFS = np.ones((L["S"], L["K"])); A_MOVE = np.zeros((L["S"], L["K"]), bool)
    A_LACK = np.ones((L["S"], L["K"]))   # lacking: <share>: without what the act requires, this share of the written chance
    CHILD_W = {"child", "children", "son", "daughter", "baby", "kid", "a child", "your child", "toddler", "pupil"}
    for si_, row_ in enumerate(L.get("notes", []) if BAT else []):
        for ki_, nt_ in enumerate(row_ or []):
            if not isinstance(nt_, dict):
                continue
            if nt_.get("death_if_fails"):
                A_DEATH[si_, ki_] = float(nt_["death_if_fails"])
            if nt_.get("kills"):
                r_ = str(nt_["kills"]).strip().lower()
                if r_ in CHILD_W:
                    raise ValueError(f"{L['names'][si_]}: kills: {r_} - a child is never a victim (Emren 2026-10-04 22:43)")
                A_KILL[si_, ki_] = ROLES.index(r_) if r_ in ROLES else -2
            if nt_.get("kills_if_fails"):   # the person named dies if the act fails (a friend who will not wake up);
                r_ = str(nt_["kills_if_fails"]).strip().lower()         # '<role> <share>': in that share of failures
                if len(r_.split()) > 1:
                    try:
                        A_KILLFS[si_, ki_] = float(r_.split()[-1]); r_ = " ".join(r_.split()[:-1])
                    except ValueError:
                        pass
                    if not 0 < A_KILLFS[si_, ki_] <= 1:
                        raise ValueError(f"{L['names'][si_]}: kills_if_fails: the share must be above 0 and at most 1")
                if r_ in CHILD_W:
                    raise ValueError(f"{L['names'][si_]}: kills_if_fails: {r_} - a child is never a victim (Emren 2026-10-04 22:43)")
                A_KILLF[si_, ki_] = ROLES.index(r_) if r_ in ROLES else -2
            if nt_.get("lacking") is not None:   # the packs (23:00): an outsider can try, but rarely wins (election night)
                A_LACK[si_, ki_] = float(nt_["lacking"])
                if not 0 < A_LACK[si_, ki_] <= 1:
                    raise ValueError(f"{L['names'][si_]}: lacking: must be a share above 0 and at most 1")
            if str(nt_.get("moves", "")).strip().lower() in ("yes", "true", "1"):   # the act moves the person (take the job abroad)
                A_MOVE[si_, ki_] = True
    AD_ON = bool((A_DEATH > 0).any()); AK_ON = bool((A_KILL != -1).any()); AKF_ON = bool((A_KILLF != -1).any())
    LACK_ON = bool((A_LACK < 1).any())
    # N1b: each option's role (women, men, keep, cross; an act that grants a title marked role= counts as that sex's act),
    # the options that name one's own gender (norm: transition, its mark, or came out in a moment only about gender), and
    # the moments that read who someone is
    IDC_ON = IDF_ON = TROLE_ON = False
    if ID2 and BAT:
        ROLE_ACT = np.array(L.get("ROLE_OPT", np.full((L["S"], L["K"]), -1)))
        TROLE_ = np.asarray(GR.get("role", np.full(NT_, -1))) if RON else np.zeros(0, int)
        TROLE_ON = bool((TROLE_ >= 0).any())
        if TROLE_ON:
            tr_ = GR["A_TITLE"]; tt_ = _uclip(tr_, 0, NT_ - 1)
            ROLE_ACT = np.where((ROLE_ACT < 0) & (tr_ >= 0) & (tr_ < NT_), TROLE_[tt_], ROLE_ACT)
        IDG = np.asarray(L.get("ID_GATE", np.zeros((L["S"], 4), bool)))
        IDF_ON = bool(IDG.any())
        COME_K = MIDX.get("came out", -1); NAMED_K = MIDX["named their gender"]
        CO_SPLIT = np.where(IDG[:, 0] & ~IDG[:, 1], 1, np.where(IDG[:, 1] & ~IDG[:, 0], 2, 0))   # came out tells: 0 all, 1 gender, 2 attraction
        TRANS_OPT = (L["MARK"] == NAMED_K) | ((L["MARK"] == COME_K) & (CO_SPLIT == 1)[:, None] & (COME_K >= 0))
        if "W_NORM" in L and WKEYS is not None:
            TRANS_OPT |= L["W_NORM"] == WKEYS.NORM_KEYS.index("transition")
        # a moment open to either mark (came out, or named their gender: growing old without hiding again): its written
        # closed: approval reads, for someone who named their own gender, how far the world accepts that (Library 10-07)
        MKBOTH_ = np.zeros(L["S"], bool)
        for c_ in L["COND"]:
            if "'came out'" in c_["rtxt"] and "'named their gender'" in c_["rtxt"]:
                MKBOTH_[c_["s"]] = True
        OPENMK_ = MKBOTH_[:, None] & (np.asarray(L["CLOSED"]) == 1)   # 1: approval (batch.WITHOUT)
        IDC_ON = bool(((ROLE_ACT >= 0) & (ROLE_ACT != 2)).any() or TRANS_OPT.any())
        COND_S = {c_["s"] for c_ in L["COND"]}
        INTIM_ = [int(x) for x in L.get("INTIM", [])]; BABY_ = SIDX.get("a baby on the way, planned or not", -1)
        PSP_ = np.asarray(P["partner_same_p"], float)

    def role_view():   # N1b: how strict the world is with each person, how far it accepts their own gender, which role it
        # expects of them (women, men): the sex they were raised as, and once they have named their own gender, that one
        # by the accepting share (a named nonbinary person's own gender carries no role, so that share expects nothing)
        rs_ = np.minimum(1.0, RS0 + (0.0 if WON else 0.5) * faith_given * I[:, FAI])   # with the world on the faith's
        # community is in the local norms already (outer world round 3, point 3)
        at_ = np.broadcast_to(np.asarray(AT0, float), (N,)).copy()   # the setting's share, or each person's with the world on
        a_ = np.where(named_g, at_, 0.0); bi_ = (~female).astype(int)
        ex_ = np.zeros((N, 2)); ex_[ar, bi_] += 1 - a_; ex_[ar, 1 - bi_] += np.where(gender_self == 1, a_, 0.0)
        return rs_, at_, ex_

    def die(n_, cause):   # the character's own death (self_death): the life is idle from now on
        if not dead[n_]:
            dead[n_] = True; died.append((int(n_), t, cause))
            if n_ in events:
                events[n_].append(dict(died=dict(age=round(t / 52, 2), cause=cause)))

    def sea_open(n_, k_):   # a crossing opens a season (a new one replaces one still running)
        if SEA_ON and ((k_ < NS and sea_had[n_, k_]) or dead[n_]):
            return
        if SEA_ON and (TH_K == k_).any():
            if k_ < NS:
                sea_had[n_, k_] = True
            sea_k[n_] = k_; sea_t0[n_] = t; sea_done[n_] = False
            sea_log.append((int(n_), t, int(k_)))

    WON = bool(P["world"]) and BAT                     # the outer world (world-build.md, "How the engine reads the world")
    MK_ON = bool(P.get("sph_marks")) and WON           # spheres phase 2: the mark of the work (world on only)
    EYES_ON_ = bool(P.get("sph_eyes")) and bool(P.get("sph_haunts")) and WON   # S3: their places read their acts (world on, with the haunts)
    ODD_ON_ = EYES_ON_ and bool(P.get("sph_odd"))      # S4: the odd one out at a place
    SHAR_ON = bool(P.get("sph_shadow")) and WON        # spheres phase 5: the shadow around a life (with shadows)
    GG_ON = bool(P.get("grey_gate")) and WON           # finishing pack, part 5: the town gone grey (moments' shadow:)
    grey_y = []                                        # its readout: each life's town's grey share per sphere, each year
    DEEP_ON = bool(P.get("sph_deep")) and WON          # spheres phase 5: the care load
    WL2_ON = bool(P.get("wl2")) and WON                # WL2: prices for workers too, a recession's hours, a disaster's cost, a pandemic year
    CLU_ON = BAT and (IDC_ON or WON)                   # closures counted in units (N1b roles, the world's laws and norms)
    WL = None; drv_h, drv_u, drv_p = P["world_harsh"], P["world_unrest"], P["world_prosper"]
    LW_ON = False; LW_T_ = None   # S7 lead_ways (world on, with sph_levers): the office titles a post is made of
    SEEN_ON = False
    BT_ON = False; btrust = None   # body_trust (world on): trust in a sphere's bodies, the People's array
    TRG_ = np.asarray(L.get("W_TRUST", np.full((L["S"], 2), -1))).reshape(-1, 2)[:L["S"]]   # body_trust's moment gate:
    TRG_S_ = np.nonzero(TRG_[:, 0] >= 0)[0]                  # (sphere, 0 low / 1 high) per moment (batch.py; -1 none)
    OWN_ON = bool(P.get("own_open")) and "OWN" in L       # v22.5, F12: the culture's own acts always on offer
    STH_ON = False; STH_SOC = None; STH_FW = None         # v22.5, F12: the start holds (world on)
    SOC_OWN = 0.0; onic = None                             # v22.5, G19w: the company a life picks (world on)
