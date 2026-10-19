# run_13_learning.py: part 13 of 18 of engine._run, the life loop.
# 4. learning channels, needs, tension, trouble and fortune.
# Lines here are _run's own, unchanged and at their own indent: engine.py joins the parts in order (engine.RUN_PARTS)
# and compiles them as one, so a name used here may be set in an earlier part. Never import or run it alone.
        # ---- 4. learning channels
        pos = delta > 0
        lens_ = w if not P["lens_want"] else (1 - P["lens_want"]) * w + P["lens_want"] * softmax(y)   # lens_want: and who one is becoming
        kap = ma * lens_ ** P["rho"]; kap /= kap.sum(1, keepdims=True) + 1e-12
        defend = P["defend_k"] * (ma * w).sum(1) / w.max(1) * (M / (M + P["M0"]))   # experienced people discount failures in what they hold
        # v6 (Library notes A5): a failure sends the person toward what the situation called for, the colors whose
        # argument it proved right, not evenly toward everything else they hold
        called = np.maximum(alpha - alpha.mean(1, keepdims=True), 0)
        called = np.where(called.sum(1, keepdims=True) > 1e-9, called / np.maximum(called.sum(1, keepdims=True), 1e-9), w)
        # Only big failures in one's own strongest ways do this (the flaw shows where life pushes back)
        ff = P["fail_fit"] * _uclip((stakes - 0.7) / 0.5, 0, 1) * _uclip((ma * w).sum(1) / w.max(1), 0, 1)
        away = (1 - ff[:, None]) * w + ff[:, None] * called
        dI = np.where(pos[:, None], P["eta"] * ldelta[:, None] * (kap - w),
                      P["eta"] * ldelta[:, None] * (1 - defend)[:, None] * (ma - away))
        if P["unusual_k"]:   # v6 (Bardi & Schwartz 2003): doing what everyone around you does says little about you
            typ = (ma * nic).sum(1) / (nic * nic).sum(1)
            dI *= _uclip(1 + P["unusual_k"] * (1 - typ), 0.5, 2.0)[:, None]
        dI[idle] = 0
        if P["own_k"] != 1.0:   # played lives: the game weighs the character's own weekly lesson
            dI = P["own_k"] * dI
        dD = np.where(pos[:, None], -ldelta[:, None] * ma, -ldelta[:, None] * defend[:, None] * ma) - P["slack"] * ma
        dD[idle] = 0
        D = np.maximum(0, D * (1 - P["D_decay"]) + dD)

        # needs: drain weekly; your niche supplies some; successful acts meet the needs
        # their ends serve; acting against a value's ends drains the needs it meets. Only the act's own ends
        # drain needs: a world that frames colors as opposed adds inner tension (peace), not deprivation (v4)
        if NM_ON:   # P4: through each person's own table
            need += -P["need_drain"] + P["need_drain"] * 0.7 * 5 * np.einsum("njc,nc->nj", NMP, nic)
            if NW_ON: nw_mark(NW_FADE)
            room = (1 - need) if P["satiate"] else 1.0
            if SH_ON:
                sh_b0 = need[:, NIDX["belonging"]].copy()
            need += 0.12 * np.maximum(stakes, P["need_floor"])[:, None] * np.where(succ[:, None], np.einsum("njc,nc->nj", NMP, np.maximum(ea, 0)), 0) * act_ * room
            need += 0.06 * np.einsum("njc,nc->nj", NMP, np.minimum(ea0, 0)) * act_
            if SH_ON:
                shared_history(sh_b0, room)
            if NW_ON: nw_mark(NW_ACT)
            # the table moves (§1): an act that worked feeds what lacked most, through its colours (one that failed, the
            # reverse, at half); habit ties the colours used to what lacks; held goals tie theirs to their domain's needs
            ep_ = np.maximum(ea, 0); sg_ = np.where(succ, 1.0, -0.5) * stakes * (~idle)
            dNM = P["nm_lr_moment"] * sg_[:, None, None] * (lack - lack.mean(1, keepdims=True))[:, :, None] * ep_[:, None, :]
            dNM += P["nm_lr_habit"] * lack[:, :, None] * (ma - 0.2)[:, None, :] * act_[:, :, None]
            gw_ = gs * (gd >= 0)
            if gw_.any():
                dNM += P["nm_lr_goal"] * np.einsum("ng,ngj,ngc->njc", gw_, KPAY[np.maximum(gd, 0)], gm - 0.2)
            NMP = NMP + dNM * (NMAP > 0)[None] + (NMAP[None] - NMP) * (np.log(2) / (52 * P["nm_back"]))
            NMP = np.clip(NMP, NM_LO[None], NM_HI[None])
            NMP = NMP * (NM_TOT / np.maximum(NMP.sum(1), 1e-9))[:, None, :]     # each colour's column keeps its total
        else:
            need += -P["need_drain"] + P["need_drain"] * 0.7 * 5 * (nic @ NMAP.T)
            if NW_ON: nw_mark(NW_FADE)
            room = (1 - need) if P["satiate"] else 1.0    # v6: a need that is nearly met gains less from each act (satiation)
            if SH_ON:
                sh_b0 = need[:, NIDX["belonging"]].copy()
            need += 0.12 * np.maximum(stakes, P["need_floor"])[:, None] * np.where(succ[:, None], np.maximum(ea, 0) @ NMAP.T, 0) * act_ * room   # v6: quiet weeks meet needs too
            need += 0.06 * (np.minimum(ea0, 0) @ NMAP.T) * act_
            if SH_ON:
                shared_history(sh_b0, room)
            if NW_ON: nw_mark(NW_ACT)
        if P["disc_win"]:   # v7 discipline: a hard thing done on purpose (the act the person meant, against the odds), most
            hw_ = tried & succ & (p_true < 0.4)          # formative in childhood as temperament is; slowly drifts back to even
            dsc[hw_] += P["disc_win"] * TST[stage[hw_]] / TST[2] * (P["disc_range"][1] - dsc[hw_])
            dsc += (1 - dsc) * (1 - 0.5 ** (1 / (52 * P["disc_back"])))
        if P["aut_self"]:   # v6: acting as oneself meets autonomy; acting against oneself drains it a little
            own_ = 0.5 * (w + softmax(y))
            concord = _uclip(2 * (ma * own_).sum(1) / own_.max(1) - 1, -0.5, 1)   # 1 = in one's strongest color, 0 = at half of it
            need[:, NIDX["autonomy"]] += P["aut_act"] * concord * (~idle) * np.where(concord > 0, room[:, NIDX["autonomy"]] if P["satiate"] else 1, 1)
            # competence: succeeding at what was hard for you, in any color; failing drains it a little
            need[:, NIDX["competence"]] += P["comp_act"] * np.where(succ, (0.5 + (1 - p_true)) * (room[:, NIDX["competence"]] if P["satiate"] else 1), -0.3 * appf_) * (~idle)
            if NW_ON: nw_mark(NW_ACT)
        if CU_ON:   # a curious, thinking life (item 7): its own goods
            ln_ = ma[:, 1] * (1 - sg0_) * (~idle)                        # C3: learning in Blue's ways, worked or not
            need[:, NIDX["meaning"]] += P["cu_learn"] * ln_; need[:, NIDX["autonomy"]] += 0.5 * P["cu_learn"] * ln_
            if NW_ON: nw_mark(NW_ACT)
            late_ = _uclip((age - 55) / 10, 0, 1) * np.maximum(sig[:, 1] - 0.3, 0)   # C2: understanding pays late
            need[:, NIDX["competence"]] += P["cu_late"] * late_; need[:, NIDX["meaning"]] += 0.5 * P["cu_late"] * late_
            if NW_ON: nw_mark(NW_AGE)
            ask_on_ = (age >= 35) & (sig[:, 1] > 0.55) & (w[:, 1] > 0.22)  # C4: the one people ask
            asked += P["cu_ask_rate"] * np.where(ask_on_, 1 - asked, -0.1 * asked)
            ak_ = P["cu_ask"] * asked * (age >= 50)
            need[:, NIDX["belonging"]] += ak_; need[:, NIDX["meaning"]] += ak_
            if NW_ON: nw_mark(NW_PEOPLE)
        duty_ = np.minimum(1, (held * I) @ DUTY)                      # needs of those the person answers for
        served = ((np.maximum(ea, 0) @ NMAP.T) * duty_).sum(1)
        need[:, NIDX["meaning"]] += P["duty_mean"] * served * succ * (~idle) * (room[:, NIDX["meaning"]] if P["satiate"] else 1)
        if NW_ON: nw_mark(NW_ACT)
        # v6: tension rebounds both ways (Emren 22:46). An act that joins colors the world reads as opposed is a bet on
        # holding both: when it works the two fit together (integration, meaning, calm); when it fails the split hurts
        # (integration loosens, stress). The more the person holds both, the bigger the stakes
        span = np.einsum("ni,ij,nj->n", ma, FRpos, ma) * (~idle) * (1 + 4 * np.einsum("ni,nij,nj->n", w, FRpos[None] * (1 - J), w))
        if P["ten_good"] or P["ten_bad"]:
            need[:, NIDX["meaning"]] += P["ten_good"] * span * succ * (room[:, NIDX["meaning"]] if P["satiate"] else 1)
            if NW_ON: nw_mark(NW_ACT)
            stress += P["ten_bad"] * span * ~succ
        reb += np.stack([span * succ, span * ~succ], 1)
        # v6 (Library notes C1, A2): a big event that goes badly feeds later trouble and leaves the person open for months;
        # one that goes well feeds later fortune (Hobfoll's loss and gain spirals)
        big = had_ev & (s == s_ev) & ~idle if P["base_rates"] else np.zeros(N, bool)
        dec = np.exp(-1 / (52 * P["clust_years"]))
        trouble = trouble * dec + big * np.maximum(-fdelta, 0)
        fortune = fortune * dec + big * np.maximum(fdelta, 0)
        wound = wound * np.exp(-1 / (52 * P["wound_years"])) + big * np.maximum(-fdelta, 0)
        B += P["ev_open"] * big * np.abs(delta)   # v6 (Bardi et al. 2009): big events, good or bad, open a person to change
