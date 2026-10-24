"""National standing (v25 lane D, the engine's switch wa_nat_climb with world_answers and the world;
chroma-engine/notes/v25/other-shapes.md section 5, chroma-world/spheres/world-fit-v2.md section 3; the routes and seats in
sphere_data.WORLD_FIT national, the climb's numbers in the realm's NATIONAL_CLIMB).

Three kinds of national standing, kept apart (decision #11): recognition (a national name: no decisions; it fades over
recognition_fade_years without new work), influence (a voice in national choices: 4 to 8 national decisions a year, while
its asset holds) and authority (a formal seat: the 8 to 12 decisions band, while held, then hold_after_years at level 3
before falling to 2). Fifteen routes, three a colour; a route's colour says whose motives it suits, never who may take
it, and nothing here reads a colour.

Who may climb: a life at a route's wider step (rung_years or more at rung 4 in a sphere, a summit title held - a title of
standing 2 or more - or a movement or firm it leads past its town). Each kind comes with base a year (x aim_x with an aim
for a route there: with aims v2, an aim on the agenda whose field is a route's aim (chroma-packs/national ROUTES) and
whose next rung is a standing-3 seat in that sphere, the climb then taking that route; without aims v2 or the pack, the
goal the life pursues in that sphere; no town-size factor, no r), authority only to a free seat: one of the routes' seats
not held by another life of the run and not one of the engine's own offices (a seat that exists already as a title, head
of government, minister, party leader, general, magnate, comes by that title's own ways). The movement road (a movement
led with movement_share or more of the country) and the money road (money and work rank) reach national influence, and
national standing (People._standing), not authority. A seat ends with its term, a fall, or age. In world answers'
phase 2 a seat held or a national name makes a life Known (its decisions band); a voice alone does not (Vision, 10-23).

The seats are Packs' catalogue titles with standing=3; while chroma-packs/national is not in the batch, a seat is the
engine's record (People.nat_view), not a title the catalogue grants. Its own dice stream; off, nothing here exists."""
import numpy as np

from world_keys import DOMAINS, SPHERES
from world_people_base import G, NEVER

KINDS = ("recognition", "influence", "authority")
# the domain a sphere's national standing is in (world_people_answers.WA_SPH_DOM, as phase 2's national push)
SPH_DOM = dict(rule="state", prot="state", comm="economy", prod="economy", learn="tech", care="institution",
               faith="belief", arts="culture", gather="culture")


class National:
    """The climb of one run's lives (People.nat, WorldLink.nat). Made by WorldLink.nat_setup()."""

    def __init__(self, PP, P, R_):
        import sphere_data as SD
        F = SD.WORLD_FIT["national"]
        self.PP = PP; N = self.N = int(PP.N)
        self.C = dict(R_.NATIONAL_CLIMB, **(P.get("wa_nat_par") or {}))
        self.routes = list(F["routes"]); self.seats = {x_["title"]: x_ for x_ in F["seats"]}
        self.by_sph = {j: [i_ for i_, r_ in enumerate(self.routes) if s_ in r_["spheres"]] for j, s_ in enumerate(SPHERES)}
        self._rng = np.random.default_rng([int(PP.seed), 7741, int(PP.run_seed)])
        self.r4y = np.zeros((N, len(SPHERES)))             # years at rung 4 in each sphere (reset when the rung falls)
        self.kind = [dict() for _ in range(N)]              # kind -> dict(route, sphere, since, ...)
        self.held = {}                                      # seat title -> life
        self.dom = np.zeros((N, len(DOMAINS)))              # the national levels (People._standing reads them)
        self.ever = np.zeros(N, bool); self.log = []
        self.mv_road = np.zeros(N, bool); self.money_road = np.zeros(N, bool)
        self._yr = -1
        self.AG = None                                      # aims v2's agenda (run_06 sets it with aims_v2 on)
        self.top = set()                                    # the batch's standing-3 titles (run_06, with the agenda)
        self.route_aim = self._routes()                     # an aim's name -> its route (chroma-packs/national ROUTES)
        self.R_ = R_; self.tsph = None                      # each summit title's spheres (run_06: summits)

    # ------------------------------------------------------------------ the roads (People._standing, monthly)
    def roads(self, mon):
        """The movement road (a movement led, members over movement_share of the country) and the money road (money
        movement and work rank): who stands on each now."""
        PP = self.PP; C = self.C
        mv = (PP.skind == G["movement"]) & (PP.srank >= 0.85)
        self.mv_road = (mv & (PP.ssize >= C["movement_share"] * C["country_people"])).any(1)
        wk = (PP.skind == G["work"]) & (PP.srank >= C["work_rank"])
        self.money_road = (np.asarray(mon, float) >= C["money"]) & wk.any(1)
        return self.mv_road, self.money_road

    # ------------------------------------------------------------------ yearly (from WorldLink.week)
    def week(self, S_):
        PP = self.PP; t = int(PP.t)
        if t % 52 != 0 or int(t // 52) == self._yr:
            return
        self._yr = int(t // 52)
        self._year(t, S_)

    def summits(self, GR, NT):
        """Each title's spheres as a summit (NT x 9 bool; standing 2 or more): an office's (LEAD_TITLES), else its
        institution's, else its sector's, and the realm's NATIONAL_SUMMIT_SPHERE for its own."""
        from world_keys import INST_KINDS, INST_SPHERE, SECTORS, SECTOR_SPHERE
        from world_people_base import LEAD_TITLES
        own = getattr(self.R_, "NATIONAL_SUMMIT_SPHERE", {})
        m = np.zeros((NT, len(SPHERES)), bool)
        for i_ in range(NT):
            if int(GR["standing"][i_]) < 2:
                continue
            nm_ = GR["names"][i_]; in_ = int(GR["institution"][i_]) if "institution" in GR else -1
            se_ = int(GR["sector"][i_]) if "sector" in GR else -1
            sp_ = (LEAD_TITLES[nm_][1] if nm_ in LEAD_TITLES else INST_SPHERE[INST_KINDS[in_]] if in_ >= 0 and INST_SPHERE[INST_KINDS[in_]]
                   else SECTOR_SPHERE[SECTORS[se_]] if se_ >= 0 else None)
            for x_ in (sp_, own.get(nm_)):
                if x_:
                    m[i_, SPHERES.index(x_)] = True
        self.tsph = m
        return m

    def _wider(self, S_):
        """Each life's spheres at a route's wider step (N x 9): rung_years at rung 4, a summit title (standing 2 or more:
        its own spheres, summits; and every sphere the life is at rung 3 or more), or a movement or firm past its town."""
        PP = self.PP; C = self.C
        rg = np.floor(np.asarray(PP.rung, float)) if hasattr(PP, "rung") else np.zeros((self.N, len(SPHERES)))
        w = self.r4y >= C["rung_years"]
        ts = S_.get("title_standing") if isinstance(S_, dict) else None
        if ts is not None:
            w |= ((np.asarray(ts, float) >= 2)[:, None] & (rg >= 3))
        tp = S_.get("title_sph") if isinstance(S_, dict) else None
        if tp is not None:   # NR1: a summit opens its own sphere, whatever its rung there (a general's army, a minister's state)
            w |= np.asarray(tp, bool)
        for g_, js_ in (("movement", ("rule", "gather")), ("work", ("comm", "prod"))):
            led = ((PP.skind == G[g_]) & (PP.srank >= 0.85) & (PP.ssize >= C["past_town"][g_])).any(1)
            for s_ in js_:
                w[:, SPHERES.index(s_)] |= led
        return w

    def _year(self, t, S_):
        PP = self.PP; C = self.C; r = self._rng; dead = np.asarray(PP.dead, bool)
        a = float(PP._age(t))
        rg = np.floor(np.asarray(PP.rung, float)) if hasattr(PP, "rung") else np.zeros((self.N, len(SPHERES)))
        self.r4y = np.where(rg >= 4, self.r4y + 1, 0.0)
        wide = self._wider(S_) & ~dead[:, None]
        goal = np.asarray(getattr(PP, "wa_gsph", np.full(self.N, -1)))
        u = r.random((self.N, 3))
        for n in range(self.N):
            k_ = self.kind[n]
            if dead[n]:
                self._end_all(n, t, "died"); continue
            js = np.nonzero(wide[n])[0]
            # what holds: influence while its asset holds (a wider step, the movement or the money road), recognition
            # fades without new work, a seat ends with its term, a fall or age
            if "influence" in k_ and not (len(js) or self.mv_road[n] or self.money_road[n]):
                self._end(n, "influence", t, "its asset no longer holds")
            if "recognition" in k_:
                if len(js):
                    k_["recognition"]["last"] = t
                elif t - k_["recognition"]["last"] >= 52 * C["recognition_fade_years"]:
                    self._end(n, "recognition", t, "faded")
            au = k_.get("authority")
            if au is not None and au.get("held", True):
                if t >= au["until"] or a >= C["seat_age"] or r.random() < C["seat_fall"]:
                    au["held"] = False; au["after"] = t; self.held.pop(au["seat"], None)
                    self.log.append(dict(n=int(n), kind="authority", what="seat ended", seat=au["seat"], age=round(a, 2)))
            elif au is not None and t - au["after"] >= 52 * C["hold_after_years"]:
                self._end(n, "authority", t, "after the seat")
            # the roads reach influence
            if (self.mv_road[n] or self.money_road[n]) and "influence" not in k_:
                j_ = SPHERES.index("rule") if self.mv_road[n] else SPHERES.index("comm")
                self._gain(n, "influence", j_, None, t, a, "movement" if self.mv_road[n] else "money")
            if not len(js) or a < 18:   # the climb is an adult's (a wider step takes years at the top in town)
                continue
            for q_, kd in enumerate(KINDS):
                if kd in k_:
                    continue
                j = int(js[r.integers(len(js))])
                b_ = C["base"][kd] if isinstance(C["base"], dict) else C["base"]
                am_, ar_ = self._aimed(n, j, goal)
                p_ = b_ * (C["aim_x"] if am_ else 1.0)
                if u[n, q_] >= p_:
                    continue
                rs = self.by_sph.get(j, [])
                if kd == "authority":
                    rs = [i_ for i_ in rs if not self.seats.get(self.routes[i_]["seats"][0], {}).get("exists", True)
                          and self.routes[i_]["seats"][0] not in self.held]
                if not rs:
                    continue
                ri_ = rs[int(r.integers(len(rs)))]   # the draw always made (the stream the same), the aimed route kept
                self._gain(n, kd, j, ar_ if ar_ in rs else ri_, t, a, "climb")
        self._levels()

    def _routes(self):
        """chroma-packs/national/fields.py ROUTES (route key -> the aim it runs through) as aim name -> route index, or
        None without the pack (then aim_x reads the goal's sphere)."""
        import os
        import importlib.util
        import batch as BA_
        p_ = os.path.join(BA_.PACK_DIR, "national", "fields.py")
        if not os.path.exists(p_):
            return None
        sp_ = importlib.util.spec_from_file_location("chroma_pack_national_routes_v25", p_)
        m_ = importlib.util.module_from_spec(sp_); sp_.loader.exec_module(m_)
        rk_ = {r_["key"]: i_ for i_, r_ in enumerate(self.routes)}
        return {aim_: rk_[k_] for k_, aim_ in (getattr(m_, "ROUTES", {}) or {}).items() if k_ in rk_}

    def _seat3(self, name):
        """A standing-3 title's sphere (the routes' seats; else the catalogue's standing 3, sphere unknown), or None."""
        x_ = self.seats.get(name)
        if x_ is not None:
            return x_.get("sphere")
        return "?" if name in self.top else None

    def _aimed(self, n, j, goal):
        """Whether the life aims at a national route in sphere j (x aim_x), and that route's index (or None). With aims
        v2 (its agenda) and the national pack's ROUTES: an aim on its agenda (held, active or paused) whose field is a
        route's aim and whose next rung names a standing-3 title in sphere j (other-shapes.md section 5). Without them:
        the goal the life pursues is in that sphere (world answers' wa_gsph)."""
        AG = self.AG
        if AG is None or self.route_aim is None:
            return bool(goal[n] == j), None
        F = AG.F; sj = SPHERES[j]
        for s_ in range(AG.MA):
            f = int(AG.f[n, s_])
            if f < 0 or int(AG.st[n, s_]) == 3:   # aims2.DROPPED
                continue
            ri = self.route_aim.get(F["names"][f])
            k = int(AG.rung[n, s_])
            if ri is None or k >= int(F["nr"][f]):
                continue
            rg = F["items"][f]["rungs"][k]
            if any(self._seat3(t_) == sj for t_ in (rg.get("any") or rg.get("names") or [])):
                return True, ri
        return False, None

    def _gain(self, n, kd, j, ri, t, a, how):
        x_ = dict(sphere=SPHERES[j], route=self.routes[ri]["key"] if ri is not None else None, since=t, last=t, how=how)
        if kd == "authority":
            seat = self.routes[ri]["seats"][0]; self.held[seat] = int(n)
            x_.update(seat=seat, held=True, until=t + 52 * int(self._rng.integers(self.C["seat_years"][0], self.C["seat_years"][1] + 1)))
        self.kind[n][kd] = x_; self.ever[n] = True
        self.log.append(dict(n=int(n), kind=kd, what="reached", sphere=SPHERES[j], route=x_["route"], seat=x_.get("seat"),
                             how=how, age=round(a, 2)))

    def _end(self, n, kd, t, why):
        x_ = self.kind[n].pop(kd, None)
        if x_ is not None:
            if kd == "authority" and x_.get("held", False):
                self.held.pop(x_["seat"], None)
            self.log.append(dict(n=int(n), kind=kd, what="ended", why=why, route=x_.get("route"), age=round(float(self.PP._age(t)), 2)))

    def _end_all(self, n, t, why):
        for kd in list(self.kind[n]):
            self._end(n, kd, t, why)

    def _levels(self):
        """The national levels in each domain (People._standing takes the larger): authority 3 in its seat's domain
        (3 for hold_after_years after the seat, then 2), influence 3 in its sphere's, recognition 2."""
        self.dom[:] = 0
        for n in range(self.N):
            for kd, x_ in self.kind[n].items():
                d_ = DOMAINS.index(SPH_DOM[x_["sphere"]])
                lv = 2 if kd == "recognition" else 3
                self.dom[n, d_] = max(self.dom[n, d_], lv)

    # ------------------------------------------------------------------ what the engine and the game read
    def national(self):
        """At national standing for world answers' phase 2: a seat held (authority) or a national voice (influence)."""
        return np.array([("influence" in k_) or bool((k_.get("authority") or {}).get("held", False)) for k_ in self.kind], bool)

    def known(self):
        """Known in world answers' phase 2 by national standing (decision of 10-23, Vision): a seat held (authority) or a
        national name (recognition). Influence alone (a voice, the money road's) is not."""
        return np.array([("recognition" in k_) or bool((k_.get("authority") or {}).get("held", False)) for k_ in self.kind], bool)

    def influence_only(self):
        return np.array([("influence" in k_) and not bool((k_.get("authority") or {}).get("held", False)) for k_ in self.kind], bool)

    def view(self, n):
        """The life's national standing, the three kinds apart: each None or dict(sphere, route, since_age, how; a seat's
        title and whether it is held), and the years at rung 4 in each sphere."""
        out = {}
        for kd in KINDS:
            x_ = self.kind[n].get(kd)
            out[kd] = None if x_ is None else dict(sphere=x_["sphere"], route=x_["route"], how=x_["how"],
                                                  since_age=round(float(self.PP._age(x_["since"])), 2),
                                                  **({"seat": x_["seat"], "held": bool(x_.get("held"))} if kd == "authority" else {}))
        out["years_at_rung4"] = {s_: int(self.r4y[n, j]) for j, s_ in enumerate(SPHERES) if self.r4y[n, j] > 0}
        return out

    def output(self):
        return dict(kinds=list(KINDS), lives=[self.view(n) for n in range(self.N)], ever=[bool(x_) for x_ in self.ever],
                    log=list(self.log), seats_held=dict(self.held))
