"""People's methods for sacred lines (S5) and seen_done (S6).

Part of class People (world_people.py), which inherits SacredMixin; moved out of world_people.py verbatim. A method
here reads module names through the imports below, the same objects world_people.py has, and self for everything on
the People."""
import sys
import numpy as np
from library import COLORS
from world_keys import HAUNT_KINDS, HEAL_TAGS, OFFER_KINDS, OFFER_ROUNDS, SACRED_KINDS, SECTORS, SPHERES
from world_people_base import (BIT, C, CAR, HAUNT_SPH, HEA, KID, KN, MON, NEVER, SAC_DEFAULT, SAC_WHO, SEEN_DEFAULT,
    SEEN_FIG, SEEN_KINDS, SEEN_WORDS, _norm)


class SacredMixin:
    # ------------------------------------------------------------------ sacred lines (S5): what a life will not sell
    def _sac_init(self, run_seed):
        """S5, sacred lines (chroma-ideas/social-mechanics.md): each life's lines (up to two, by kind: promise, truth,
        own_say, loved, home, the five colours in the Canon's order), the record that forms them (how long the lead
        colour has led, the acts in each colour's ways that cost something real), the offers waiting for their moment,
        the wounds of crossing, and its own random stream. The offers come from sphere_data.OFFER (the Outer world's
        tags on sphere and C3 events)."""
        import sphere_data as SD
        N = self.N
        self.sac_par = {**SAC_DEFAULT, **dict((getattr(self.W, "p", None) or {}).get("sacred_par") or {})}
        self.sac_line = np.full((N, 2), -1, np.int64)     # each line's kind (index into SACRED_KINDS), -1 none
        self.sac_t = np.full((N, 2), NEVER, np.int64)     # the week it formed
        self.sac_wound = np.full((N, 2), NEVER, np.int64)  # the week it was crossed and not yet healed (NEVER: whole)
        self.sac_held = np.zeros((N, 2), np.int64); self.sac_crossed = np.zeros((N, 2), np.int64)   # times held, crossed
        self.sac_paid = np.zeros((N, C), np.int64)        # acts in each colour's ways that cost something real
        self.sac_lead = np.full(N, -1, np.int64); self.sac_lead_t = np.full(N, NEVER, np.int64)   # the lead colour, since
        self.sac_lead_y = np.zeros((N, C))                # years each colour has led (the colour-even audit)
        self.sac_lost = np.zeros((N, 2))                  # money and ties not had by holding (the audit)
        self.sac_tragic = np.full(N, -1, np.int8)         # -1 not drawn, 0 no, 1 may meet a tragic trade-off, 2 met it
        self.sac_q = {}                                   # n -> offers and amends waiting for their moment (dicts)
        self.sac_ref = {}                                 # (n, offer key) -> times refused (the next one is raised)
        self.sac_am = {}                                  # (n, line slot) -> amends moments offered since its wound
        self.sac_fxq = []                                 # offers decided off-screen, for the engine (sac_take)
        self._sac_rng = np.random.default_rng([self.seed, 93, self.run_seed])
        self._sac_i = len(getattr(self.W, "sph_ev_log", ()))   # the world's town events already read
        self._sac_lm = -1                                 # the month last counted
        self.sac_n = {}                                   # counts for the checks (not saved)
        self.sac_col = self.iperm.copy()                  # each kind's colour in this life's frame (W U B R G relabelled)
        self._sac_ev = {}                                 # sphere_data.EV index -> offer key
        ek = {f"{e['sphere']}.{e['key']}": i for i, e in enumerate(SD.EV)}
        for k, v in SD.OFFER["events"].items():
            bad = [x for x in v["lines"] if x not in SACRED_KINDS]
            if bad or v["kind"] not in OFFER_KINDS or not (v["who"] in SAC_WHO or v["who"].startswith("sector:")):
                raise ValueError(f"offer {k}: unknown line kinds {bad}, kind {v['kind']!r} or who {v['who']!r}")
            if k in ek:
                self._sac_ev[ek[k]] = k

    def _sac_count(self, key, m=1):
        self.sac_n[key] = self.sac_n.get(key, 0) + int(np.sum(m))

    def _sac_fit(self, ns, who, t):
        """The lives ns an offer is made to by its who: word (far_sides.json's words, read for the character)."""
        a = self._age(t); held = self.held; res = self.res
        emp = held[ns, CAR] if held.shape[1] > CAR else np.zeros(len(ns), bool)
        own = self.own_home[ns] | (self.cls[ns] >= 2)
        if who == "any":
            return np.ones(len(ns), bool) & (a >= 16)
        if who.startswith("sector:"):
            return emp & (self.psector[ns] == SECTORS.index(who[7:]))
        m = dict(in_work=emp, out_of_work=~emp & (18 <= a < 65), owner=own, renter=~own, poor=res[ns, MON] < 0.15,
                 comfortable=res[ns, MON] >= 0.4, young=np.full(len(ns), a < 30), old=np.full(len(ns), a >= 65),
                 ill=res[ns, HEA] < 0.5, parent=held[ns, KID] if held.shape[1] > KID else np.zeros(len(ns), bool))[who]
        return np.asarray(m, bool) & (a >= 16)

    def sac_offer(self, ns, key, t=None, reach=None):
        """An offer (sphere_data.OFFER[key]) made in town to the lives ns: those it fits (who:), whose line it touches,
        each with chance reach, wait for its moment (lapse weeks). Two held lines touched at once make a tragic
        trade-off for a life drawn to meet one (at most one, in at most sacred_par tragic of lives); else the first
        line of the offer's that they hold."""
        import sphere_data as SD
        t = self.t if t is None else t; sp = self.sac_par
        o = SD.OFFER["events"][key]; kinds = [SACRED_KINDS.index(x) for x in o["lines"]]
        ns = np.asarray(ns, np.int64)
        if not len(ns) or self._age(t) < sp["age"]:
            return
        ns = ns[~self.dead[ns] & (self.sac_line[ns] >= 0).any(1)]
        if not len(ns):
            return
        ns = ns[self._sac_fit(ns, o["who"], t)]
        tch = (self.sac_line[ns][:, :, None] == np.asarray(kinds)[None, None, :]).any(2)   # n x 2: the line is touched
        tch &= (self.sac_held[ns] + self.sac_crossed[ns]) < sp["known"]   # (a line answered known times, held or
        # crossed, is settled around them: no more offers come for it; v22.4 fix round: counting only holds kept offers
        # coming to lines that were crossed, so lives that cross more (Black- and Red-led) held more offers and paid more)
        ns, tch = ns[tch.any(1)], tch[tch.any(1)]
        r_ = self._sac_rng.random(len(ns)) < (sp["reach"] if reach is None else reach)
        for n_, tc_ in zip(ns[r_], tch[r_]):
            n_ = int(n_); q_ = self.sac_q.setdefault(n_, [])
            if any(x_.get("key") == key for x_ in q_):
                continue
            if tc_.all() and self.sac_tragic[n_] == 1:
                q_.append(dict(kind="tragic", key=key, slots=[0, 1], due=int(t), until=int(t) + int(sp["lapse"])))
                self._sac_count("tragic offered")
                continue
            sl_ = [j_ for j_ in range(2) if tc_[j_]]
            sl_.sort(key=lambda j_: kinds.index(int(self.sac_line[n_, j_])))   # the offer's own first line
            nr_ = self.sac_ref.get((n_, key), 0)
            q_.append(dict(kind="sacred", key=key, slots=[sl_[0]], due=int(t), until=int(t) + int(sp["lapse"]),
                           round=1 if nr_ else 0, size=float(min(sp["size_max"], 2.0 ** nr_))))
            self._sac_count("offered")

    def _sac_week(self, t):
        """The town events of the week that carry an offer (sphere_data.OFFER) reach the people living in that town (a
        whole-society event, everyone); C3's institution events come through WorldLink (to the staff). Offers and
        amends past their time lapse."""
        log = getattr(self.W, "sph_ev_log", None)
        if log is not None and len(log) > self._sac_i:
            rows = np.asarray(log[self._sac_i:]).tolist(); self._sac_i = len(log)
            for _, i_, l_ in rows:
                k_ = self._sac_ev.get(int(i_))
                if k_ is None:
                    continue
                here = ~self.dead & ((self.loc == l_) if l_ >= 0 else True)
                if self._xsoc:   # a life abroad does not hear its home town's offers
                    here &= self.soc == self.soc_home
                self.sac_offer(np.nonzero(here)[0], k_, t)
        for n_ in list(self.sac_q):
            keep_ = [x_ for x_ in self.sac_q[n_] if x_["until"] >= t and not self.dead[n_]]
            gone_ = [x_ for x_ in self.sac_q[n_] if x_ not in keep_]
            if keep_:
                self.sac_q[n_] = keep_
            else:
                del self.sac_q[n_]
            for x_ in gone_:   # an offer whose moment never came is decided off-screen, by the character's own odds
                self._sac_count("lapsed")
                if x_["kind"] != "amends" and not self.dead[n_] and self.sac_par["quiet"]:
                    self.sac_quiet(n_, x_, t)

    def sac_quiet(self, n, item, t=None):
        """An offer or tragic trade-off with no moment for it (none in the Library for that line, or its moment never
        came within lapse weeks): the character decides it off-screen by their own odds (sac_odds; at a tragic one
        tragic_w), with every effect but the turning point's lesson (there is no act to learn from). The engine applies
        it with the week's act (sac_take)."""
        t = self.t if t is None else t
        if item["kind"] == "tragic":
            tw_ = np.asarray(self.sac_par["tragic_w"], float)
            tag_ = int(np.searchsorted(np.cumsum(tw_ / tw_.sum()), self._sac_rng.random(), side="right"))
            tag_ = min(tag_, 2)
        else:
            tag_ = 1 if self._sac_rng.random() >= self.sac_odds(item) else 0
        q_ = self.sac_q.setdefault(n, [])
        if item not in q_:
            q_.append(item)
        ev = self.sac_resolve(n, item, tag_, False, None, t)
        ev["quiet"] = True
        self.sac_fxq.append(ev)
        self._sac_count("quiet")
        return ev

    def sac_take(self):
        """The off-screen offers decided since the last call (events for engine.py's sac_fx), each handed over once."""
        out, self.sac_fxq = self.sac_fxq, []
        return out

    def _sac_month(self, t):
        """The lead colour and how long it has led; a line forms where the lead has held lead years and paid acts."""
        if self._sac_lm == t:
            return
        dt_ = 0.0 if self._sac_lm < 0 else (t - self._sac_lm) / 52.0
        self._sac_lm = t
        ld = np.argmax(self.w, 1)
        self.sac_lead_y[np.arange(self.N), self.sac_lead] += dt_ * (self.sac_lead >= 0) * ~self.dead
        ch = ld != self.sac_lead
        self.sac_lead_t = np.where(ch, t, self.sac_lead_t); self.sac_lead = ld
        self._sac_form(np.nonzero(~self.dead)[0], t)

    def _sac_form(self, ns, t):
        """S5: a line forms in the lead colour once it has led sacred_par lead years and the life has paid a real cost
        paid times for acts in its ways (sacred_par age and over, at most lines). Its form is the colour's kind."""
        sp = self.sac_par
        if self._age(t) < sp["age"] or not len(ns):
            return
        ld = self.sac_lead[ns]; kd = self.perm[np.maximum(ld, 0)]   # the lead colour's kind (canonical colour)
        ok = ((ld >= 0) & (t - self.sac_lead_t[ns] >= 52 * sp["lead"]) & (self.sac_paid[ns, np.maximum(ld, 0)] >= sp["paid"])
              & ((self.sac_line[ns] >= 0).sum(1) < sp["lines"]) & ~(self.sac_line[ns] == kd[:, None]).any(1))
        for n_, k_ in zip(ns[ok], kd[ok]):
            j_ = int(np.argmax(self.sac_line[n_] < 0))
            self.sac_line[n_, j_] = k_; self.sac_t[n_, j_] = t
            self._sac_count(f"line {SACRED_KINDS[k_]}")
            if j_ == 1 and self.sac_tragic[n_] < 0:   # the second line: may this life meet a tragic trade-off (1 in 10)
                self.sac_tragic[n_] = int(self._sac_rng.random() < sp["tragic"])
            if self.watch[n_]:
                self.events.append(dict(n=int(n_), t=int(t), kind="sacred", what="line", line=SACRED_KINDS[k_],
                                        colour=COLORS[int(self.sac_col[k_])]))

    def sac_act(self, idx, ma, cost, t=None):
        """The week's acts (engine.py, after their costs): an act in a colour's ways (its mix's lead) that cost something
        real counts toward a line in that colour (from age 12), and heals a wound of that colour's line crossed before
        it (an act of amends in the line's ways: a real cost paid for it again)."""
        t = self.t if t is None else t
        idx = np.asarray(idx, np.int64); cost = np.asarray(cost, bool)
        if not len(idx) or self._age(t) < 12:
            return []
        c_ = np.argmax(np.asarray(ma), 1)
        n2, c2 = idx[cost], c_[cost]
        np.add.at(self.sac_paid, (n2, c2), 1)
        out = []
        for n_, cc_ in zip(n2, c2):
            for j_ in range(2):
                k_ = int(self.sac_line[n_, j_])
                if k_ >= 0 and self.sac_col[k_] == cc_ and NEVER < self.sac_wound[n_, j_] < t:
                    out.append(self._sac_heal(int(n_), j_, t, "amends in its ways"))
        self._sac_form(np.unique(n2), t)
        return out

    def _sac_heal(self, n, j, t, how):
        self.sac_wound[n, j] = NEVER
        q_ = self.sac_q.get(n)
        if q_:   # its amends moment is no longer waiting
            self.sac_q[n] = [x_ for x_ in q_ if not (x_["kind"] == "amends" and x_["slots"] == [j])]
        self._sac_count("healed")
        ev = dict(n=int(n), t=int(t), kind="sacred", what="healed", how=how, line=SACRED_KINDS[int(self.sac_line[n, j])],
                  colour=COLORS[int(self.sac_col[int(self.sac_line[n, j])])], heal=float(self.sac_par["heal"]))
        return ev   # (the engine reports it: engine.py sac_fx)

    def sac_due(self, t=None):
        """[(n, item)]: the first offer or amends of each life waiting for its moment and due by now."""
        t = self.t if t is None else t
        out = []
        for n_, q_ in self.sac_q.items():
            for x_ in q_:
                if x_["due"] <= t <= x_["until"] and not self.dead[n_]:
                    out.append((int(n_), x_)); break
        return out

    def sac_odds(self, item):
        """The character's own pick at an offer: holds with this chance (the refusal odds)."""
        sp = self.sac_par
        if item.get("kind") != "sacred":
            return None
        import sphere_data as SD
        g_ = SD.OFFER["events"][item["key"]]["gesture"]
        return float(min(sp["cap"], (sp["gesture"] if g_ else sp["refuse"]) + sp["doubling"] * np.log2(max(item["size"], 1.0))))

    def sac_info(self, n, item):
        """What the game names in a sacred, tragic or amends moment: the line or lines (kind and colour), the offer
        (the Outer world's words, its kind and gesture), the round, its size and the refusal odds."""
        import sphere_data as SD
        lines = [dict(line=SACRED_KINDS[int(self.sac_line[n, j])], colour=COLORS[int(self.sac_col[int(self.sac_line[n, j])])],
                      since=int(self.sac_t[n, j]), wounded=bool(self.sac_wound[n, j] > NEVER)) for j in item["slots"]]
        out = dict(kind=item["kind"], lines=lines)
        if item.get("key"):
            o = SD.OFFER["events"][item["key"]]
            out.update(offer=o["offer"], offer_key=item["key"], offer_kind=o["kind"], gesture=bool(o["gesture"]))
        if item["kind"] == "sacred":
            out.update(round=OFFER_ROUNDS[int(item["round"])], size=float(item["size"]), refuse=self.sac_odds(item))
        return out

    def sac_resolve(self, n, item, tag, idle, ma, t=None):
        """The moment that answered an offer, a tragic trade-off or amends: tag is the picked option's line: (0 hold,
        1 cross), tragic: (0 a, 1 b, 2 torn) or heal: (0 amends, 1 reflect, 2 not_yet), -1 untagged (an untagged
        option or doing nothing holds a line, is torn at a trade-off, and heals nothing). Returns the event the engine
        applies: held lines' costs (money, ties not had), crossed lines' wounds (stress, a shadow seed, a turning point)."""
        t = self.t if t is None else t; sp = self.sac_par
        q_ = self.sac_q.get(n, [])
        if item in q_:
            q_.remove(item)
            if not q_:
                self.sac_q.pop(n, None)
        ev = dict(n=int(n), t=int(t), kind="sacred", moment=item["kind"], key=item.get("key"), held=[], crossed=[],
                  money=0.0, ties=0.0, wound=0.0, seed=0.0, colours=[], healed=[])
        if item["kind"] == "amends":
            j = item["slots"][0]
            if tag in (0, 1) and self.sac_wound[n, j] > NEVER:
                h_ = self._sac_heal(n, j, t, HEAL_TAGS[tag])
                ev["healed"].append(h_["colour"]); ev["heal"] = h_["heal"]
            elif self.sac_wound[n, j] > NEVER:   # left for later: another amends moment a year on (at most amends_max)
                self._sac_amends(n, j, t, again=True)
            ev["what"] = "healed" if ev["healed"] else "not yet"
            return ev
        import sphere_data as SD
        o = SD.OFFER["events"][item["key"]]
        if item["kind"] == "tragic":
            a_, b_ = self._sac_tragic_order(n, item)
            hold, cross, f_ = ({0: ([a_], [b_], 1.0), 1: ([b_], [a_], 1.0)}.get(tag, ([], [a_, b_], 0.5)))
            self.sac_tragic[n] = 2
        else:
            hold, cross, f_ = ([], item["slots"], 1.0) if tag == 1 and not idle else (item["slots"], [], 1.0)
        for j in hold:
            dm_, dt_ = sp["hold"][o["kind"]]; sz_ = float(item.get("size", 1.0))
            ev["money"] += dm_ * sz_; ev["ties"] += dt_ * sz_
            self.sac_lost[n] += (dm_ * sz_, dt_ * sz_); self.sac_held[n, j] += 1
            col_ = int(self.sac_col[int(self.sac_line[n, j])]); ev["held"].append(COLORS[col_])
            if item["kind"] == "sacred":
                self.sac_ref[(n, item["key"])] = self.sac_ref.get((n, item["key"]), 0) + 1
                if self.sac_ref[(n, item["key"])] == 1:   # the raised offer comes after a first refusal
                    lo_, hi_ = sp["raised"]
                    d_ = int(t) + int(self._sac_rng.integers(lo_, hi_ + 1))
                    self.sac_q.setdefault(n, []).append(dict(kind="sacred", key=item["key"], slots=list(item["slots"]),
                                                             due=d_, until=d_ + int(sp["lapse"]), round=1,
                                                             size=float(min(sp["size_max"], 2.0 * item["size"]))))
            if getattr(self, "eyes_on", False):   # S3 (their places' eyes): holding the line moves their name
                oh_ = np.zeros(C); oh_[col_] = 1.0
                self.eyes_see(np.array([n]), oh_[None], np.array([1.0]), "sacred")
            self._sac_count("held")
        for j in cross:
            col_ = int(self.sac_col[int(self.sac_line[n, j])])
            self.sac_crossed[n, j] += 1; self.sac_wound[n, j] = t
            ev["crossed"].append(COLORS[col_]); ev["colours"].append(col_)
            ev["wound"] += sp["wound"] * f_; ev["seed"] = sp["seed"] * f_
            self._sac_amends(n, j, t)
            self._sac_count("crossed")
        ev["what"] = "tragic" if item["kind"] == "tragic" else "crossed" if cross else "held"
        ev["round"] = OFFER_ROUNDS[int(item.get("round", 0))]
        return ev   # (the engine applies and reports it: engine.py sac_fx)

    def _sac_tragic_order(self, n, item):
        """A tragic moment's a and b: the slots of its sacred: kinds in the moment's order (set by WorldLink)."""
        ab = item.get("ab") or item["slots"]
        return int(ab[0]), int(ab[1])

    def _sac_amends(self, n, j, t, again=False):
        """After a wound (or an amends moment left for later), amends wait their weeks: a reflection or an act of amends."""
        sp = self.sac_par
        nt_ = (self.sac_am.get((n, j), 0) if again else 0) + 1
        if nt_ > sp["amends_max"]:
            return
        self.sac_am[(n, j)] = nt_
        lo_, hi_ = sp["amends"]
        d_ = int(t) + (int(sp["amends_again"]) if again else int(self._sac_rng.integers(lo_, hi_ + 1)))
        self.sac_q.setdefault(n, []).append(dict(kind="amends", key=None, slots=[j], due=d_, until=d_ + int(sp["lapse"])))

    # ------------------------------------------------------------------ seen_done (S6): paths and ways seen walked
    # (chroma-ideas/social-mechanics.md, S6 "Seen it done"; Bandura 1977, 1997; Bell, Chetty et al. 2019; Chetty et al.
    # 2022; Lockwood and Kunda 1997). What a cast member carries here: a job or not (emp) in a sector, a standing 0-3
    # (stand), a partner (mpart) and children (nkids), their colours as the character reads them (read). Each walks one
    # catalogue title at work: the career of their sector at their standing (a pack ladder's rung where it has one),
    # drawn by the title's share with a fixed hash of who they are (no random draw); partner and children are one
    # ladder each, every title of the kind (not a facet, open by 30), so a married parent shows the whole way. Seen holding a path counts as a success once, at the weight they
    # were seen with (more if they come closer); gaining it again (work found, a standing gained, a partner, a child)
    # is a success; losing it (work lost before 64, a standing lost, a partnership ended) a failure. The public figures
    # walk the title of their role (SEEN_FIG): rising into the role is a success, a scandal or a fall a failure.
    def _seen_init(self):
        N, K = self.N, self.K
        self.sd_par = {**SEEN_DEFAULT, **dict((getattr(self.W, "p", None) or {}).get("seen_par") or {})}
        self.sd_ec = np.zeros((N, C)); self.sd_fc = np.zeros((N, C))   # exposure and failures seen per colour way
        self.sd_ctop = np.full((N, C), -1, np.int32); self.sd_ctopw = np.zeros((N, C))   # ... its strongest model (cast
        self.sd_ctopk = np.zeros((N, C), np.int8)                                          # id), weight, SEEN_WORDS index
        self._sd_uid = np.full((N, K), -1, np.int32)      # last quarter's cast, to read what changed since
        self._sd_emp = np.zeros((N, K), bool); self._sd_mp = np.zeros((N, K), bool)
        self._sd_nk = np.zeros((N, K), np.int8); self._sd_st = np.zeros((N, K), np.int8)
        self._sd_t = np.full((N, K, 3), -1, np.int32)    # the title each walks at work; 1 on partner and children
        self._sd_w = np.zeros((N, K, 3), np.float32)     # the weight each model's path was credited at
        self._sd_wc = np.zeros((N, K), np.float32)       # ... and their colour way
        self._sd_figs = set()                             # public figures seen in their role (credited once)
        self._sd_li = len(getattr(self.W, "log", ()))    # the world's log entries already read (scandals, falls)
        self._sd_saved = None                             # a load's per-life records, applied when the titles come
        self.seen_setup(None)

    def seen_setup(self, cat):
        """seen_done: the title catalogue the paths are counted in (the link passes the engine's L["ROLES"]: names,
        kindname, sector, standing, share, refines, ages; None: none yet). Arrays per life and title index:
        sd_e exposure (successes x weight - failures x fail x weight), sd_f failures seen (weighted), sd_top the
        strongest model's cast id (-1 none; a public figure f as -(f + 2)), sd_topw its weight and sd_topk its word
        (SEEN_WORDS: 0 seen, 1 wrong, 2 far)."""
        N = self.N; NT = int(cat["NT"]) if cat is not None else 0
        self.sd_names = list(cat["names"])[:NT] if NT else []; self.sd_nt = NT
        kn = list(cat["kindname"][:NT]) if NT else []
        self.sd_kind = np.array([KN.index(k_) if k_ in KN else -1 for k_ in kn], np.int64)   # the commitment each title is in
        self.sd_e = np.zeros((N, NT), np.float32); self.sd_f = np.zeros((N, NT), np.float32)
        self.sd_top = np.full((N, NT), -1, np.int32); self.sd_topw = np.zeros((N, NT), np.float32)
        self.sd_topk = np.zeros((N, NT), np.int8)   # the strongest model's word: 0 seen, 1 wrong, 2 far (SEEN_WORDS)
        self._sd_pool = {}; self._sd_pk = {1: (np.zeros(0, np.int64), np.zeros(0)), 2: (np.zeros(0, np.int64), np.zeros(0))}
        self._sd_fig = {}
        if NT:
            sec = np.asarray(cat["sector"])[:NT]; std = np.asarray(cat["standing"])[:NT]
            sh = np.maximum(np.asarray(cat["share"], float)[:NT], 1e-4)
            ref = np.asarray(cat["refines"])[:NT]; ages = np.asarray(cat["ages"], float)[:NT]
            car = np.array([k_ == "career" for k_ in kn])

            def pool(ids):
                ids = np.asarray(ids, np.int64)
                cw = np.cumsum(sh[ids]); return ids, cw / cw[-1] if len(ids) else cw
            for s_ in range(len(SECTORS)):   # work: the careers of the sector at the cast member's standing
                for st_ in range(4):
                    cs_ = car & (sec == s_)
                    c_ = np.nonzero(cs_ & ((std == st_) if st_ >= 1 else (std <= 0)))[0]
                    if not len(c_) and st_ >= 1:
                        c_ = np.nonzero(cs_ & (std >= 1))[0]
                    if not len(c_):
                        c_ = np.nonzero(cs_)[0]
                    self._sd_pool[s_ * 4 + st_] = pool(c_)
            for q_ in (1, 2):   # partner and children: one ladder each, the kind's own titles (not a facet, open by 30)
                c_ = np.nonzero(np.array([k_ == SEEN_KINDS[q_] for k_ in kn]) & (ref < 0) & (ages[:, 0] <= 30))[0]
                self._sd_pk[q_] = pool(c_)
            ix = {x_: i_ for i_, x_ in enumerate(self.sd_names)}
            self._sd_fig = {r_: ix[x_] for r_, x_ in SEEN_FIG.items() if x_ in ix}
        if self._sd_saved:
            ix = {x_: i_ for i_, x_ in enumerate(self.sd_names)}
            for n_, d_ in self._sd_saved.items():
                for x_, v_ in d_.items():
                    if x_ in ix:
                        self.sd_e[n_, ix[x_]], self.sd_f[n_, ix[x_]], self.sd_top[n_, ix[x_]], self.sd_topw[n_, ix[x_]] = v_[:4]
                        self.sd_topk[n_, ix[x_]] = v_[4] if len(v_) > 4 else 0
            self._sd_saved = None
        sn, sk = np.nonzero(self._sd_uid >= 0)   # (after a load) the paths the cast walked when last read
        self._sd_t[sn, sk] = self._sd_titles(sn, sk)
        self._sd_lift()

    def _sd_hash(self, n, k, salt):
        """A fixed number in [0, 1) for cast member (n, k) and a salt: their name index, hashed (no random draw)."""
        x = (self.nm[n, k].astype(np.int64) * 2654435761 + salt * 40503 + 977) % 4294967296
        return x / 4294967296.0

    def _sd_titles(self, n, k):
        """The title cast members (n, k) walk at work by sector and standing (len x 3, -1 none), and 1 on the partner
        and children ladders (whether they walk each now is read from emp, mpart and nkids)."""
        out = np.full((len(n), 3), -1, np.int32)
        if not self.sd_nt or not len(n):
            return out
        sec = self.sector[n, k].astype(np.int64); st = np.clip(self.stand[n, k].astype(np.int64), 0, 3)
        pl = np.where(sec >= 0, sec * 4 + st, -1); u = self._sd_hash(n, k, 1)
        for p_ in np.unique(pl[pl >= 0]).tolist():
            ids, cw = self._sd_pool.get(p_, (np.zeros(0, np.int64), None))
            if len(ids):
                m_ = pl == p_
                out[m_, 0] = ids[np.minimum(np.searchsorted(cw, u[m_], side="right"), len(ids) - 1)]
        for q_ in (1, 2):   # partner and children: one ladder each (every title of the kind, _sd_pk), marked 1
            out[:, q_] = 1 if len(self._sd_pk[q_][0]) else -1
        return out

    def _sd_rung(self):
        """Each life's own rung, the highest of its spheres' (N2; 0 without the haunts' rungs)."""
        rg = getattr(self, "rung", None)
        return np.floor(rg.max(1)) if rg is not None else np.zeros(self.N)

    def _seen_w(self, t, live):
        """The weight each cast member's walk is seen with (N x K): close people (layers 1 and 2) 1; regulars at the
        life's haunts .3, one of another class only through a gather haunt (the places that mix walks of life), by the
        town's gather.mixing; x .3 for a model far above (3 or more rungs: their standing 0-3 reads as regular to leader,
        a haunt's keeper as leader; or 25 or more years older). Also returns that far mask (N x K)."""
        p = self.sd_par; N, K = self.N, self.K
        close = live & (self.c >= self.P["layer_c"][1])
        reg = live & ~close & ((self.rmask & BIT["regular"]) != 0)
        w = close * np.float32(p["close"])
        if reg.any():
            other = self.mcls != self.cls[:, None]
            at_g = np.zeros((N, K), bool)
            hp = getattr(self.W, "hp_s", None); sh = getattr(self, "shnt", None)
            if hp is not None and sh is not None:
                H = len(HAUNT_KINDS); P_ = hp.shape[2]
                gj = (sh >= 0) & (HAUNT_SPH[np.maximum(sh, 0) // P_ % H] == SPHERES.index("gather"))
                for j_ in np.nonzero(gj.any(0))[0]:
                    at_g |= gj[:, j_][:, None] & (((self.mset >> self.mset.dtype.type(j_)) & 1) > 0)
            try:
                mx = np.asarray(self.W.sph_state("gather.mixing"), float)[np.minimum(self.loc, self.n_loc - 1)]
            except Exception:
                mx = np.full(N, 0.5)
            mw = np.minimum(1.0, p["mix"] * mx)[:, None]
            w = w + reg * np.float32(p["regular"]) * np.where(other, np.where(at_g, mw, 0.0), 1.0)
        mr = 1 + np.clip(self.stand.astype(np.int64), 0, 3)
        mr = np.where((self.rmask & BIT["keeper"]) != 0, 4, mr)
        far = (mr - self._sd_rung()[:, None] >= p["far_rungs"]) | (self._mage(t) - self._age(t) >= p["far_years"])
        return (w * np.where(far, p["far"], 1.0)).astype(np.float32), far

    def _sd_add(self, nn, ti, x, f=None, who=None, ww=None, far=None):
        """Credit x (and failures f) to lives nn on titles ti; who, ww, far: the model's id, weight and whether they
        count as far above, for the strongest model on each path (sd_top, sd_topw, sd_topk: SEEN_WORDS' index). A
        success makes them the strongest when they weigh more (or already are): seen, or far; a failure seen when they
        weigh as much or more (or already are): wrong."""
        ok = ti >= 0
        nn, ti, x = nn[ok], ti[ok], x[ok]
        if not len(nn):
            return
        np.add.at(self.sd_e, (nn, ti), x)
        if f is not None:
            np.add.at(self.sd_f, (nn, ti), f[ok])
        if who is not None:
            who, ww = who[ok], ww[ok]
            fr = np.zeros(len(nn), bool) if far is None else np.broadcast_to(far, ok.shape)[ok]
            key = nn.astype(np.int64) * max(self.sd_nt, 1) + ti
            o_ = np.lexsort((-ww, key)); ks_ = key[o_]
            first = o_[np.r_[True, ks_[1:] != ks_[:-1]]]
            n1, t1 = nn[first], ti[first]; tw_ = self.sd_topw[n1, t1]; same_ = self.sd_top[n1, t1] == who[first]
            b_ = (ww[first] >= tw_) | same_ if f is not None else (ww[first] > tw_) | same_
            n1, t1, i1 = n1[b_], t1[b_], first[b_]
            self.sd_top[n1, t1] = who[i1]; self.sd_topw[n1, t1] = np.maximum(ww[i1], np.where(same_[b_], tw_[b_], 0))
            self.sd_topk[n1, t1] = 1 if f is not None else np.where(fr[i1], 2, 0)

    def _seen_q(self, t):
        """seen_done, each quarter: what the cast was seen doing since the last (successes and failures on each path,
        and on the colour ways as the character reads each model), the public figures, then the felt-odds lifts."""
        p = self.sd_par; N, K = self.N, self.K
        live = self.used & self.lv & ~self.dead[:, None]
        same = live & (self.uid == self._sd_uid)
        tnew = np.full((N, K, 3), -1, np.int32)
        ln, lk = np.nonzero(live)
        tnew[ln, lk] = self._sd_titles(ln, lk)
        if self._age(t) >= p["from_age"]:
            w, far = self._seen_w(t, live)
            fresh = live & ~same                              # a new face in the slot: nothing of theirs credited yet
            self._sd_w[fresh] = 0.0; self._sd_wc[fresh] = 0.0
            emp_ok = (self._mage(t) < 64)
            hold = np.stack([self.emp, self.mpart, self.nkids > 0], -1) & live[..., None]
            gain = np.stack([same & self.emp & (~self._sd_emp | (self.stand > self._sd_st)),
                             same & self.mpart & ~self._sd_mp, same & (self.nkids > self._sd_nk)], -1)
            lose = np.stack([same & self._sd_emp & ((~self.emp & emp_ok) | (self.stand < self._sd_st)),
                             same & ~self.mpart & self._sd_mp, np.zeros((N, K), bool)], -1)
            wq = w[..., None]
            pos = np.where(gain, wq, np.where(hold & (wq > self._sd_w), wq - self._sd_w, 0.0)) * (wq > 0)
            neg = np.where(lose, wq, 0.0)
            self._sd_w = np.where(hold | gain, np.maximum(self._sd_w, wq), self._sd_w).astype(np.float32)
            for q_ in range(3):
                ids_ = [None] if q_ == 0 else self._sd_pk[q_][0].tolist()   # work: their own title; else the kind's ladder
                nn, kk = np.nonzero(pos[..., q_] > 0)
                for i_ in ids_ if len(nn) else ():
                    ti_ = tnew[nn, kk, q_] if i_ is None else np.where(tnew[nn, kk, q_] >= 0, i_, -1)
                    self._sd_add(nn, ti_, p["win"] * pos[nn, kk, q_], who=self.uid[nn, kk], ww=w[nn, kk], far=far[nn, kk])
                nn, kk = np.nonzero(neg[..., q_] > 0)
                for i_ in ids_ if len(nn) else ():   # a failure, on the path as they walked it before
                    ti_ = self._sd_t[nn, kk, q_] if i_ is None else np.where(self._sd_t[nn, kk, q_] >= 0, i_, -1)
                    self._sd_add(nn, ti_, -p["fail"] * neg[nn, kk, q_], f=neg[nn, kk, q_], who=self.uid[nn, kk],
                                 ww=w[nn, kk])
            ha, ga = hold.any(-1), gain.any(-1)
            cw_ = np.where(ga, w, np.where(ha & (w > self._sd_wc), w - self._sd_wc, 0.0))
            cn_ = np.where(lose.any(-1), w, 0.0)
            self._sd_wc = np.where(ha | ga, np.maximum(self._sd_wc, w), self._sd_wc).astype(np.float32)
            if cw_.any() or cn_.any():
                rd = self.read.astype(float)
                self.sd_ec += np.einsum("nk,nkc->nc", p["win"] * cw_ - p["fail"] * cn_, rd)
                self.sd_fc += np.einsum("nk,nkc->nc", cn_, rd)
                # the strongest model in each colour way: the most weight x their share of it, as for the paths
                for v_, fl_ in ((cw_, False), (cn_, True)):
                    if not v_.any():
                        continue
                    x_ = np.where(v_ > 0, w, 0.0)[..., None] * rd; kb_ = x_.argmax(1); xb_ = np.take_along_axis(x_, kb_[:, None], 1)[:, 0]
                    ub_ = self.uid[np.arange(N)[:, None], kb_]; same_ = self.sd_ctop == ub_
                    b_ = (xb_ > 0) & (((xb_ >= self.sd_ctopw) if fl_ else (xb_ > self.sd_ctopw)) | same_)
                    self.sd_ctop = np.where(b_, ub_, self.sd_ctop)
                    self.sd_ctopw = np.where(b_, np.maximum(xb_, np.where(same_, self.sd_ctopw, 0)), self.sd_ctopw)
                    fb_ = far[np.arange(N)[:, None], kb_]
                    self.sd_ctopk = np.where(b_, 1 if fl_ else np.where(fb_, 2, 0), self.sd_ctopk).astype(np.int8)
            self._seen_figs(t)
        self._sd_uid = np.where(live, self.uid, -1).astype(np.int32)
        self._sd_emp = self.emp.copy(); self._sd_mp = self.mpart.copy(); self._sd_nk = self.nkids.copy()
        self._sd_st = self.stand.copy(); self._sd_t = tnew
        self._sd_lift()

    def _seen_figs(self, t):
        """seen_done: the public figures, seen by every life at .05 (x .3 when far above: always a leader's rung, or 25
        or more years older): a figure seen in their role a success, once; a scandal or a fall a failure."""
        W = self.W; p = self.sd_par
        log = getattr(W, "log", None)
        try:
            role = np.asarray(W.fig_role, np.int64); pie = np.asarray(W.fig_pie, float).reshape(-1, C)
            act = np.asarray(W.fig_alive, bool) & np.asarray(getattr(W, "fig_active", W.fig_alive), bool)
            born = np.asarray(W.fig_born, float)
        except AttributeError:
            return
        names = getattr(sys.modules.get(type(W).__module__), "FIG_ROLES", None)
        ev = [(f_, 1) for f_ in np.nonzero(act)[0].tolist() if f_ not in self._sd_figs]
        self._sd_figs.update(f_ for f_, _ in ev)
        if log is not None:
            if len(log) < self._sd_li:   # another society's world (a move abroad): its log from here on
                self._sd_li = len(log)
            for e_ in log[self._sd_li:]:
                if e_.get("domain") == "figure" and e_.get("kind") in ("scandal", "falls"):
                    f_ = int((e_.get("value") or {}).get("fig", -1))
                    if 0 <= f_ < len(role):
                        ev.append((f_, -1))
            self._sd_li = len(log)
        if not ev:
            return
        ln = np.nonzero(~self.dead)[0]
        if not len(ln):
            return
        rg = self._sd_rung()[ln]; a = self._age(t)
        for f_, sg_ in ev:
            nm_ = names[int(role[f_])] if names is not None and 0 <= role[f_] < len(names) else None
            ti = self._sd_fig.get(nm_, -1)
            far = (4 - rg >= p["far_rungs"]) | ((t - born[f_]) / 52.0 - a >= p["far_years"])
            wv = p["figure"] * np.where(far, p["far"], 1.0)
            x_ = np.sin((f_ + 1) * 12.9898 + np.arange(C)[None] * 78.233 + ln[:, None] * 0.618034 + self.run_seed * 0.414214) * 43758.5453
            sl_ = _norm((x_ - np.floor(x_) + 0.2)[:, self.perm])   # the character's reading, as figure_view reads it
            rd = _norm(0.5 * pie[f_][None] + 0.3 * self.lens[ln] + 0.2 * sl_)
            if sg_ > 0:
                self.sd_ec[ln] += p["win"] * wv[:, None] * rd
                if ti >= 0:
                    self._sd_add(ln, np.full(len(ln), ti), p["win"] * wv, who=np.full(len(ln), -(f_ + 2), np.int32), ww=wv,
                                 far=far)
            else:
                self.sd_ec[ln] -= p["fail"] * wv[:, None] * rd; self.sd_fc[ln] += wv[:, None] * rd
                if ti >= 0:
                    self._sd_add(ln, np.full(len(ln), ti), -p["fail"] * wv, f=wv, who=np.full(len(ln), -(f_ + 2), np.int32),
                                 ww=wv)

    def _sd_lift(self):
        """The felt-odds lifts the engine adds (seen_done): per life and title sd_lt, per life and colour way sd_lc:
        lift x min(exposure, cap) (none below 0) - fail_lift x min(failures seen, fail_cap)."""
        p = self.sd_par
        self.sd_lt = (p["lift"] * np.clip(self.sd_e, 0, p["cap"]) - p["fail_lift"] * np.minimum(self.sd_f, p["fail_cap"])).astype(np.float32)
        self.sd_lc = p["lift"] * np.clip(self.sd_ec, 0, p["cap"]) - p["fail_lift"] * np.minimum(self.sd_fc, p["fail_cap"])

    def seen_dom(self, n):
        """seen_done: per commitment (career, partner, children, community, faith) the share of cap its best seen path
        has reached (0..1), for a new dream's domain (engine, 4d)."""
        out = np.zeros(len(KN))
        if self.seen_on and self.sd_nt:
            e_ = np.clip(self.sd_e[n], 0, self.sd_par["cap"]) / self.sd_par["cap"]
            for d_ in range(len(KN)):
                m_ = self.sd_kind == d_
                if m_.any():
                    out[d_] = float(e_[m_].max())
        return out

    def _sd_word(self, n, top, k, e, f):
        """The Library's word (SEEN_WORDS) and the model for one path or way: none when nothing was seen on it."""
        if top == -1 or (e <= 0 and f <= 0):
            return dict(kind="none")
        d_ = dict(kind=SEEN_WORDS[int(k)])
        if top >= 0:
            k_ = self._slot(n, top)
            d_.update(who=int(top), role=self._rname(n, k_) if k_ >= 0 else None)
        else:
            d_.update(figure=-int(top) - 2)
        return d_

    def seen_model(self, n, ti):
        """seen_done, for the game's option row ("She has seen it done: her aunt Mira" / "No one she knows has done
        this"; the Library's earth_spheres.SEEN words): title ti's path, kind (SEEN_WORDS: seen, the strongest model on
        it succeeded; wrong, they were seen failing; far, they count x .3, far above or 25 years older; none, nothing
        seen on it), who (that model's cast id; a public figure gives figure, their id, instead), their role if still
        in the cast, the exposure, failures seen and the felt-odds lift. None for no title."""
        ti = int(ti)
        if not self.seen_on or ti < 0 or ti >= self.sd_nt:
            return None
        e_, f_ = float(self.sd_e[n, ti]), float(self.sd_f[n, ti])
        return dict(self._sd_word(n, int(self.sd_top[n, ti]), self.sd_topk[n, ti], e_, f_), path=self.sd_names[ti],
                    exposure=round(e_, 2), failures=round(f_, 2), lift=round(float(self.sd_lt[n, ti]), 3))

    def seen_way(self, n, c):
        """seen_done: the same for colour way c (an option on no path, by its leading way): kind, who, way (the colour
        key), exposure, failures seen and the felt-odds lift on that way."""
        if not self.seen_on:
            return None
        c = int(c); e_, f_ = float(self.sd_ec[n, c]), float(self.sd_fc[n, c])
        return dict(self._sd_word(n, int(self.sd_ctop[n, c]), self.sd_ctopk[n, c], e_, f_), way=COLORS[c],
                    exposure=round(e_, 2), failures=round(f_, 2), lift=round(float(self.sd_lc[n, c]), 3))

    def seen_paths(self, n, top=None):
        """seen_done, for other parts (A15's dream moments): life n's seen paths, most seen first, each as seen_model
        gives it plus domain (the commitment the title is in, None for a status). The arrays behind it: sd_e, sd_f,
        sd_top, sd_topw, sd_topk (N x titles, the engine's title indices); sd_ec, sd_fc, sd_ctop, sd_ctopw, sd_ctopk
        (N x colours); sd_lt, sd_lc the felt-odds lifts; seen_dom(n) the share per commitment."""
        if not self.seen_on:
            return []
        ix = np.nonzero((self.sd_e[n] != 0) | (self.sd_f[n] > 0))[0]
        ix = ix[np.argsort(-self.sd_e[n, ix], kind="stable")][:top]
        out = []
        for ti in ix.tolist():
            d_ = self.seen_model(n, ti)
            d_["domain"] = KN[int(self.sd_kind[ti])] if self.sd_kind[ti] >= 0 else None
            out.append(d_)
        return out

    def seen_dream(self, n, dom):
        """seen_done: for a new dream about commitment dom (engine 4d), the seen path it was seeded from: the best seen
        title of that commitment and its strongest model, as an event dict (kind "dream", who, path); None if none."""
        if not self.seen_on or not self.sd_nt or dom < 0:
            return None
        m_ = np.nonzero((self.sd_kind == int(dom)) & (self.sd_e[n] > 0))[0]
        if not len(m_):
            return None
        ti = int(m_[np.argmax(self.sd_e[n, m_])]); tp = int(self.sd_top[n, ti])
        if tp == -1:
            return None
        d_ = self._sd_word(n, tp, 0, 1.0, 0.0)
        d_["kind"] = "dream"; d_["path"] = self.sd_names[ti]
        return d_
