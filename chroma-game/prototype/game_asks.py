"""Game's methods for v24 asks (chroma-ideas/next-table-2026-10-19/plan.md section 7: "asks chosen by what matters to the
character now: their aims, lacking needs, and the people at stake. That way each ask is pivotal from their point of view,
while the outer world keeps drifting them between asks"), behind GAME ask_matter (0, off: every moment weighs as before).
How often to be asked stays the player's setting (key f); this changes which moments are asked, not how many.

Part of class Game (game.py), which inherits AsksMixin. Read-only: what it reads draws nothing, so with ask_matter at 0
every life plays as before. Steering between asks (GAME steer_between) is the player's: while they hold a lean, each
moment that is not asked has the character's own pick drawn again with it, as a light steer at a moment does, and costs
what it changed."""
import numpy as np

from game_base import E, GAME, KNAMES
from game_words import accept_word, clash_with, reluctance

PEOPLE_KINDS = ("partner", "children", "community")   # a commitment to people (foresee.PEOPLE_KINDS)
MATTER_SOON = 0.6                                     # a moment that matters this much may be asked as soon as a life event


class AsksMixin:
    def _matters(self, loc, s):
        """How much moment s matters to the character now, 0 to 1, and why: (score, dict(kind, say)) or (0.0, None).
        An option leads into the next step of an aim they hold (1); an option feeds a need they lack, by how low it is
        (up to .8); an option starts or ends a tie to people, a partner, children or a community (.6). The highest wins."""
        best = (0.0, None)
        mask = np.asarray(loc["mask"][0], bool) & ~np.asarray(loc["do_nothing"][0], bool)
        if GAME["aims"]:
            aw = self.aim_ways_view(loc) if hasattr(self, "aim_ways_view") else {}
            ws = [w for k, x in aw.items() if mask[k] for w in x]
            if ws:
                best = (1.0, dict(kind="aim", say=f"a step toward their aim, {ws[0]['aim']}"))
        if "need" in loc and best[0] < 0.8:
            need = np.asarray(loc["need"][0], float)
            fed = np.zeros(len(need))
            for k in np.nonzero(mask)[0]:
                fed = np.maximum(fed, E.NMAP @ np.maximum(loc["e"][0, k], 0))
            lack = GAME["hind_thin"]                   # a need under this is one they lack (the option row's "lift")
            low = [(float(need[j]), j) for j in range(len(need)) if fed[j] > 0.05 and need[j] < lack]
            if low:
                lv, j = min(low)
                sc = 0.4 + 0.4 * (1 - lv / lack)
                if sc > best[0]:
                    best = (round(sc, 3), dict(kind="need", say=f"something they lack, {E.NEEDS[j]}"))
        if best[0] < 0.6:
            com = np.asarray(loc["L"]["COMMIT"][s])[mask]
            ks = sorted({KNAMES[int(x)] for x in com if x >= 0 and KNAMES[int(x)] in PEOPLE_KINDS})
            if ks:
                best = (0.6, dict(kind="people", say=f"the people in their life ({ks[0]})"))
        return best

    # ------------------------------------------------------------------ steering between asks
    def steer_set(self, c):
        """The player leans them toward color c (a letter) until the next ask, or STEER_YEARS at most; None lets go."""
        if not GAME["steer_between"]:
            return False
        self._steer = None if c is None else dict(color=c.upper(), until=self.t + STEER_YEARS * 52, n=0, moved=0)
        return True

    def steer_view(self):
        st = getattr(self, "_steer", None)
        return None if st is None else dict(color=st["color"], weeks_left=max(0, int(st["until"] - self.t)), moments=st["n"],
                                             moved=st["moved"])

    def _steer_between(self, t, loc, a):
        """At a moment not put to the player, while a lean is held: their own pick drawn again with it (_light_steer),
        and a pick it changed carries a light steer's cost (the act's reluctance x the share of its odds the lean gave
        it). Returns the pick to send on."""
        st = getattr(self, "_steer", None)
        if st is None:
            return a
        if t >= st["until"]:
            self._steer = None
            self._say(f"{self.name} goes their own way again.", 0, "steer")
            return a
        if bool(loc["recon"][0]):
            return a                                    # a commitment's reconsideration is theirs alone
        mask = np.asarray(loc["mask"][0], bool); seen = np.asarray(loc["seen"][0], bool) & mask
        dn = np.asarray(loc["do_nothing"][0], bool); U = np.asarray(loc["U"][0], float)
        own = int(a[0])
        ks = [int(k) for k in np.nonzero(seen)[0]]
        k, lt = self._light_steer(loc, dict(by_idx={k_: None for k_ in ks + [own]}), st["color"])
        st["n"] += 1
        if k is None or k == own:
            return a
        Ubest = max([float(U[own])] + [float(U[k_]) for k_ in ks])
        u_dn = max([float(U[k_]) for k_ in range(len(mask)) if mask[k_] and dn[k_]] or [-np.inf])
        gaps = [Ubest - float(U[k_]) for k_ in ks if k_ != own and not dn[k_]]
        ref = max(GAME["rel_ref"], float(np.median(gaps)) if gaps else 0.0)
        clash = [] if dn[k] else clash_with(self._colors(loc, k), self._prev_label)
        rel0 = reluctance(Ubest - float(U[k]), ref, u_dn - float(U[k]), bool(clash)) * self._own_k(loc, k)
        rel = rel0 * lt["share"]
        self._force = dict(rel=rel, closed=False, idx=k, acc=accept_word(rel0), trust=self._trust_on(loc, k), light=lt)
        st["moved"] += 1
        self.history["steers"].append(dict(age=round(t / 52, 2), kind="between", colors=self._colors(loc, k), era=0.0,
                                           lean=st["color"]))
        a = a.copy(); a[0] = k
        return a

    # ------------------------------------------------------------------ talking to them before a big moment
    def talk(self, k):
        """The player argues for option k at a big moment (an ask from a life event, or one that matters MATTER_SOON or
        more), once a moment (plan section 7, Vision's call 10-19). The character answers in a line of their own, and
        that option's reluctance falls for this pick only: more when it fits their heart or head and leads toward an aim,
        less when it goes against who they are; a tendency, never a wall. It costs a little autonomy. Returns
        dict(line, fall) or dict(error)."""
        cp = self.pending
        if not GAME["talk"] or cp is None:
            return dict(error="not now")
        if not cp.get("big"):
            return dict(error="talking it over is for the big moments")
        if cp.get("talked") is not None:
            return dict(error="you have already talked this one over")
        o = cp["by_idx"].get(int(k))
        if o is None or o["colors"] == "-":
            return dict(error="no such option")
        fit = max(float(o.get("heart") or 0.0), float(o.get("head") or 0.0))   # the share heart or head would give it
        aim = bool(o.get("aims"))
        fall = float(np.clip(GAME["talk_k"] * (0.2 + 0.5 * fit + 0.2 * aim - 0.2 * bool(o.get("clash"))), 0.0, 0.8))
        o["rel"] = round(float(o["rel"]) * (1 - fall), 4)
        if o["idx"] != cp["own"]:
            o["acc"] = accept_word(o["rel"])
        if self.loc is not None and "need" in self.loc:
            j = E.NEEDS.index("autonomy")
            self.loc["need"][0, j] = max(0.0, float(self.loc["need"][0, j]) - GAME["talk_cost"])
        dr = o.get("drivers") or {}
        pro = [nm for side in ("heart", "head") for nm, x in dr.get(side, []) if x > 0]
        con = [nm for side in ("heart", "head") for nm, x in dr.get(side, []) if x < 0]
        if fall >= 0.45:
            line = f"“You may be right. {('There is ' + pro[0] + ' in it.') if pro else 'I can see it.'}”"
        elif fall >= 0.25:
            line = f"“Maybe.{(' ' + cap1(con[0]) + ' gives me pause, but I hear you.') if con else ' I will think about it.'}”"
        else:
            line = f"“I hear you, but {con[0] if con else 'it is not me'}.”"
        cp["talked"] = dict(idx=int(o["idx"]), line=line, fall=round(fall, 2))
        self.history.setdefault("talks", []).append((round(self.age(), 1), o["label"], round(fall, 2)))
        return dict(line=line, fall=round(fall, 2))


def cap1(s):
    return s[:1].upper() + s[1:]


STEER_YEARS = 2                                       # a lean held between asks lasts at most this long
